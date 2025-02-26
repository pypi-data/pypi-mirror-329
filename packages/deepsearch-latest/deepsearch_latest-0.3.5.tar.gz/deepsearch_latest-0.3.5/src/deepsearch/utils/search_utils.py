import asyncio
import aiohttp
import logging
from typing import Sequence, Union
import mcp.types as types

from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.openrouter_utils import split_and_extract_information
from deepsearch.utils.async_utils import log_cancellation

logger = logging.getLogger("deepsearch-mcp")


@log_cancellation
async def perform_search_analysis(
    query: str,
    pinecone_client: PineconeManager,
    cloudflare_uploader: CloudflareUploader,
    request_id: str,
    inflight_requests: dict,
    model: str = "openai/o3-mini",
    deepthink: bool = False
) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Perform search analysis using Pinecone and Cloudflare
    """
    try:
        logger.info("Starting document retrieval and analysis...")

        # Step 1: Get search results and fetch documents
        search_results = pinecone_client.search_documents(
            query, min_normalized_score=0.2)
        logger.info(f"Retrieved {len(search_results)} documents")

        # Step 2: Fetch documents
        documents = await async_fetch_all_documents(search_results, cloudflare_uploader)

        # Step 3: Process documents with OpenRouter
        processed_results = await async_process_documents_with_openrouter(
            query=query,
            documents=documents,
            model=model,
            deepthink=deepthink
        )

        # Utility to strip out repeated "No relevant information..." lines
        def _clean_extracted_info(info: str) -> str:
            """
            Remove repeated "No relevant information found in the document." statements
            and return what's left. If nothing is left, it means there's no real info.
            """
            cleaned = info.replace(
                "No relevant information found in the document.", "")
            return cleaned.strip()

        # Filter out documents that end up with no actual content
        filtered_processed_results = {}
        for doc_path, raw_info in processed_results.items():
            cleaned_info = _clean_extracted_info(raw_info)
            # If there's still something left besides whitespace, we keep it; otherwise we skip
            if cleaned_info:
                filtered_processed_results[doc_path] = cleaned_info

        # If no documents had relevant information, return empty list
        if not filtered_processed_results:
            logger.info("No documents contained relevant information")
            return [types.TextContent(type="text", text="No results found for the given query.")]

        # Combine results from filtered documents
        all_results = []
        for doc_path, info in filtered_processed_results.items():
            # Get the matching normalized score from search_results
            score = next(
                entry['normalized_score']
                for entry in search_results
                if entry['cloudflare_path'] == doc_path
            )
            all_results.append({
                'source': doc_path,
                'score': score,
                'extracted_info': info
            })

        # Sort by score in descending order
        results = sorted(all_results, key=lambda x: x['score'], reverse=True)

        # Format output
        formatted_output = []
        for result in results:
            section = [
                f"\nSource: {result['source']}",
                f"Score: {result['score']:.3f}",
                "Extracted Information:",
                f"{result['extracted_info']}",
                "=" * 80
            ]
            formatted_output.append("\n".join(section))

        # Return as TextContent object
        return [types.TextContent(type="text", text="\n".join(formatted_output))]

    except Exception as e:
        logger.error(f"Error in perform_search_analysis: {str(e)}")
        raise


@log_cancellation
async def async_fetch_all_documents(search_results, cloudflare_uploader) -> dict:
    """Fetch all documents concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            cloudflare_uploader._fetch_document_text(doc['cloudflare_path'])
            for doc in search_results
        ]
        texts = await asyncio.gather(*tasks)
        return {
            result['cloudflare_path']: text
            for result, text in zip(search_results, texts)
            if text
        }


@log_cancellation
async def async_process_documents_with_openrouter(query: str, documents: dict, model: str = "openai/o3-mini", deepthink: bool = False) -> dict:
    """Process all documents with OpenRouter concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            split_and_extract_information(
                query, text, session=session, deepthink=deepthink)
            for text in documents.values()
        ]
        results = await asyncio.gather(*tasks)
        return {
            doc_path: result
            for (doc_path, _), result in zip(documents.items(), results)
        }
