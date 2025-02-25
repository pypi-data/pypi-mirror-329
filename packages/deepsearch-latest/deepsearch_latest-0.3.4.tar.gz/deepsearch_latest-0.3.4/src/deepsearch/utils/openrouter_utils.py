import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from deepsearch.utils.prompts import information_extraction_prompt, deep_analysis_prompt
import logging
import tiktoken
from typing import List
from deepsearch.utils.async_utils import log_cancellation

logger = logging.getLogger("deepsearch-mcp")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Add these constants at the top with your other imports
API_URL = "https://openrouter.ai/api/v1/chat/completions"


async def make_api_call(prompt, model="openai/o3-mini", temperature=0.1, session=None, max_retries=5, base_delay=1):
    """Make API call with exponential backoff retry logic."""
    logger.info(f"Making API call to OpenRouter with model: {model}")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "max_tokens": 100000,
        "temperature": temperature
    }

    should_close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        should_close_session = True

    try:
        for attempt in range(max_retries):
            try:
                async with session.post(API_URL, json=data, headers=headers) as response:
                    if response.status == 200:
                        resp_json = await response.json()
                        if 'choices' in resp_json:
                            logger.info(
                                "Successfully received response from OpenRouter")
                            return resp_json['choices'][0]['message']['content']
                    elif response.status == 429:  # Rate limit exceeded
                        delay = base_delay * (2 ** attempt)
                        logger.warning(
                            f"Rate limit exceeded. Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Error response (status {response.status}): {error_text}")

                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Attempt {attempt+1} failed. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)

            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(
                        f"All retry attempts failed. Final error: {str(e)}")
                    raise
                delay = base_delay * (2 ** attempt)
                logger.warning(
                    f"Error occurred: {str(e)}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
    finally:
        if should_close_session:
            await session.close()

    raise Exception("Max retries exceeded")


@log_cancellation
async def test_concurrent_calls():
    # Create three different messages
    messages = [
        "What is the meaning of life?",
        "Tell me a joke",
        "What's the weather like?"
    ]

    # Create tasks for concurrent execution
    tasks = [make_api_call(msg) for msg in messages]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Print results
    for i, result in enumerate(results):
        print(f"\nResponse {i + 1} Content:")
        print(result)


def make_image_api_call(image_base64: str, prompt: str, model: str = "anthropic/claude-3.5-sonnet"):
    """Make an API call with both text and image content."""
    return {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "headers": {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        "json": {
            "model": model,
            "max_tokens": 100000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }
    }


@log_cancellation
async def split_and_extract_information(
    query: str,
    document: str,
    session=None,
    deepthink: bool = False,
    max_tokens: int = 50000,
    overlap: int = 500
):
    """Split document into smaller chunks and extract information concurrently."""
    # Initialize tokenizer
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Tokenize full document
    tokens = enc.encode(document)

    # Create smaller overlapping chunks
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        if end >= len(tokens):
            chunks.append(tokens[start:])
        else:
            chunks.append(tokens[start:end + overlap])
        start = end

    # Convert chunks back to text and create batches
    text_chunks = [enc.decode(chunk) for chunk in chunks]

    logger.info(f"Processing document in {len(text_chunks)} chunks")

    # Create a single session if none provided
    if session is None:
        session = aiohttp.ClientSession()

    # Process all chunks truly concurrently
    async def process_chunk(chunk):
        try:
            formatted_prompt = information_extraction_prompt.format(
                query=query, document=chunk)
            # Use model based on deepthink flag
            model_name = "openai/o1" if deepthink else "openai/o3-mini"
            return await make_api_call(formatted_prompt, model=model_name, session=session)
        except Exception as e:
            logger.error(f"Error processing chunk: {str(e)}")
            return ""

    # Create and gather all tasks at once
    tasks = [process_chunk(chunk) for chunk in text_chunks]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out errors and combine results
    valid_results = [r for r in results if isinstance(r, str)]
    return " ".join(valid_results)


@log_cancellation
async def extract_information(
    query: str,
    document: str,
    session=None,
    deepthink: bool = False
):
    """
    Make an async call to retrieve relevant information using the
    'information_extraction_prompt'. The final result is returned directly.

    Parameters:
        query (str): The user query
        document (str): The document content to be processed
        session (aiohttp.ClientSession, optional): The existing session (if any)
        deepthink (bool): Whether the extraction is for deepthink mode (uses 'openai/o1')
                          or for standard analysis mode (uses 'openai/o3-mini')
    """
    logger.info("Starting information extraction from document")

    # Choose model based on deepthink flag
    model_name = "openai/o1" if deepthink else "openai/o3-mini"

    formatted_prompt = information_extraction_prompt.format(
        query=query,
        document=document
    )

    result = await make_api_call(formatted_prompt, model=model_name, session=session)

    logger.info("Completed information extraction")
    return result


@log_cancellation
async def perform_deep_analysis(
    query: str,
    extracted_info: str,
    session=None,
    pinecone_client=None,
    cloudflare_uploader=None,
    request_id=None,
    inflight_requests=None
):
    """
    Perform a deeper analysis of the extracted information to uncover patterns,
    perform calculations, and generate insights. Uses a more powerful model (o1)
    for complex reasoning and calculations.
    """
    logger.info("Starting deep analysis of extracted information")
    formatted_prompt = deep_analysis_prompt.format(
        query=query,
        extracted_info=extracted_info
    )

    # Make the initial API call
    initial_analysis = await make_api_call(formatted_prompt, model="openai/o1", session=session)

    # No look for "SUGGESTED FOLLOW-UP PROMPT:" — just return
    logger.info("Completed deep analysis (no second search).")
    return initial_analysis


if __name__ == "__main__":
    asyncio.run(test_concurrent_calls())
