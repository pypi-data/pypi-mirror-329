import logging
import re
import os
from typing import Sequence, Union, List, Dict, Any
from enum import Enum
import mcp.types as types
from mcp.server import Server
from deepsearch.utils.search_utils import async_fetch_all_documents, async_process_documents_with_openrouter
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.async_utils import log_cancellation
from datetime import datetime
from pathlib import Path
from deepsearch.utils.openrouter_utils import perform_deep_analysis, make_api_call

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepsearch-mcp")


class ToolName(str, Enum):
    QUICK_SEARCH = "quick-search"
    REMEMBER = "remember"
    DEEP_RESEARCH = "deep-research"


ServerTools = [
    types.Tool(
        name=ToolName.QUICK_SEARCH,
        description="Quickly searches across database documents to find relevant information for your query.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A detailed, self-contained query that thoroughly explains the context, background, and specific aspects of what you're looking for. Include any relevant dates, names, technical terms, or specific details that could help narrow down the search. The query should be written as a complete question or set of questions that can stand alone without requiring additional context from prior conversation history."
                }
            },
            "required": ["query"],
        },
    ),
    types.Tool(
        name=ToolName.REMEMBER,
        description="Saves a memory to the knowledge base.",
        inputSchema={
            "type": "object",
            "properties": {
                "memory_text": {
                    "type": "string",
                    "description": "Text content to be remembered"
                }
            },
            "required": ["memory_text"],
        },
    ),
    types.Tool(
        name=ToolName.DEEP_RESEARCH,
        description="""Performs an interactive research process with clarification steps. This tool enables a back-and-forth conversation between the user and the search system to refine the query and retrieve the most relevant information.

IMPORTANT: ALWAYS start with stage="CLARIFICATION" for the initial call.

The tool works in stages:
1. CLARIFICATION: Initial stage that continues until the system explicitly determines it has enough information
2. SEARCH: Only used when the system confirms it has enough information to perform a search
3. REFINE_SEARCH: REQUIRED step after SEARCH where the user reviews and confirms the sources
4. ANSWER: Only used after the user has confirmed the sources in the REFINE_SEARCH stage

Each response will include:
- RESULTS: Information retrieved from the search
- NEXT_STEPS: Instructions for Claude on what to do next
- NEXT_STAGE: The stage to use in the next tool call

IMPORTANT FLOW REQUIREMENTS:
- The CLARIFICATION stage will continue for multiple rounds until the system explicitly determines it has enough information
- After SEARCH, you MUST proceed to REFINE_SEARCH to get user confirmation of sources
- Only proceed to ANSWER after the user has reviewed and confirmed the sources

Follow the NEXT_STEPS instructions in each response to determine how to proceed.""",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query from the user."
                },
                "user_input": {
                    "type": "string",
                    "description": "Additional input from the user in response to clarification questions or feedback on search results."
                },
                "stage": {
                    "type": "string",
                    "description": "The current stage of the interaction. IMPORTANT: ALWAYS use 'CLARIFICATION' for the initial call.",
                    "enum": ["CLARIFICATION", "SEARCH", "REFINE_SEARCH", "ANSWER"],
                    "default": "CLARIFICATION"
                }
            },
            "required": ["query"],
        },
    ),
]


@log_cancellation
async def perform_search_analysis(
    query: str,
    pinecone_client: PineconeManager,
    cloudflare_uploader: CloudflareUploader,
    request_id: str,
    inflight_requests: dict,
    model: str,
    deepthink: bool = False
) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Perform search analysis using Pinecone and Cloudflare
    """
    try:
        inflight_requests[request_id] = "running"

        if not query:
            logger.error("Empty query provided")
            raise ValueError("Query parameter is required")

        logger.info("Starting document retrieval and analysis...")

        # Step 1: Get search results and fetch documents
        search_results = pinecone_client.search_documents(
            query, min_normalized_score=0.2)
        logger.info(f"Retrieved {len(search_results)} documents")

        if inflight_requests.get(request_id) == "cancelled":
            return []

        # Step 2: Fetch documents
        documents = await async_fetch_all_documents(search_results, cloudflare_uploader)

        if inflight_requests.get(request_id) == "cancelled":
            return []

        # Step 3: Process documents with OpenRouter
        processed_results = await async_process_documents_with_openrouter(
            query=query,
            documents=documents,
            model=model,
            deepthink=deepthink
        )

        if inflight_requests.get(request_id) == "cancelled":
            return []

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
            inflight_requests[request_id] = "done"
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

        # Format output for MCP
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

        inflight_requests[request_id] = "done"
        return [types.TextContent(type="text", text="\n".join(formatted_output))]

    except Exception as e:
        logger.error(f"Error in perform_search_analysis: {str(e)}")
        inflight_requests[request_id] = "error"
        raise


@log_cancellation
async def deep_research(
    query: str,
    stage: str,
    request_id: str,
    pinecone_client: PineconeManager,
    cloudflare_uploader: CloudflareUploader,
    inflight_requests: dict,
    user_input: str = ""
) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Perform an interactive search with clarification steps.

    The function maintains state between calls using request_id and handles
    different stages of the interaction process.
    """
    try:
        from deepsearch.utils.prompts import (
            clarification_assessment_prompt,
            search_refinement_prompt,
            final_answer_prompt
        )

        inflight_requests[request_id] = "running"

        # Store state in a module-level variable
        if not hasattr(deep_research, 'state'):
            deep_research.state = {}

        # Check if this is the first call for this request_id and force CLARIFICATION stage
        if request_id not in deep_research.state:
            # This is the first call for this request_id
            if stage != "CLARIFICATION":
                logger.warning(
                    f"First call for request {request_id} should use CLARIFICATION stage, but got {stage}. Forcing CLARIFICATION.")
                stage = "CLARIFICATION"

            # Initialize state for this request
            deep_research.state[request_id] = {
                "original_query": query,
                "refined_query": query,
                "conversation_history": [],
                "search_history": []
            }

        state = deep_research.state[request_id]

        # Update conversation history with user input if provided
        if user_input:
            state["conversation_history"].append({
                "role": "user",
                "content": user_input
            })

        # Format conversation history for prompts
        conversation_text = "\n".join([
            f"{'Assistant' if item['role'] == 'assistant' else 'User'}: {item['content']}"
            for item in state["conversation_history"]
        ])

        # Handle different stages
        if stage == "CLARIFICATION":
            # Get source summaries based on query
            search_results = pinecone_client.search_documents(
                query, min_normalized_score=0.2)

            # Format results with source and summary only
            summaries = []
            for result in search_results:
                summaries.append({
                    'source': result['cloudflare_path'],
                    'score': result['normalized_score'],
                    'summary': result['summary']
                })

            # Format summaries for prompt
            summaries_text = "\n".join([
                f"Source: {s['source']}\nScore: {s['score']:.3f}\nSummary: {s['summary']}"
                for s in summaries[:10]  # Limit to top 10 for prompt size
            ])

            # Determine if clarification is needed
            assessment = await make_api_call(
                clarification_assessment_prompt.format(
                    query=query,
                    summaries=summaries_text,
                    conversation_history=conversation_text
                ),
                model="openai/o3-mini"
            )

            # Store the summaries
            state["current_summaries"] = summaries

            # Parse the assessment to determine next steps
            ready_for_search = "READY_FOR_SEARCH: Yes" in assessment

            if not ready_for_search:
                # Extract clarification questions
                questions_match = re.search(r"CLARIFICATION_QUESTIONS:(.*?)(?:EXPLANATION:|$)",
                                            assessment, re.DOTALL)
                explanation_match = re.search(
                    r"EXPLANATION:(.*?)$", assessment, re.DOTALL)

                questions = questions_match.group(1).strip(
                ) if questions_match else "Could you provide more details about your query?"
                explanation = explanation_match.group(
                    1).strip() if explanation_match else ""

                # Store this interaction in conversation history
                state["conversation_history"].append({
                    "role": "assistant",
                    "content": f"I need more information: {explanation}\n\nQuestions: {questions}"
                })

                # Format response with clear sections
                response = (
                    f"RESULTS:\n"
                    f"I found some potentially relevant sources, but I need more information to provide the best results.\n\n"
                    f"{explanation}\n\n"
                    f"CLARIFICATION_QUESTIONS:\n{questions}\n\n"
                    f"NEXT_STEPS:\n"
                    f"1. Present the clarification questions to the user\n"
                    f"2. Collect their response\n"
                    f"3. Call this tool again with their response\n\n"
                    f"NEXT_STAGE: CLARIFICATION"
                )
            else:
                # Extract refined query
                refined_query_match = re.search(r"REFINED_QUERY:(.*?)(?:EXPLANATION:|$)",
                                                assessment, re.DOTALL)
                explanation_match = re.search(
                    r"EXPLANATION:(.*?)$", assessment, re.DOTALL)

                refined_query = refined_query_match.group(
                    1).strip() if refined_query_match else query
                explanation = explanation_match.group(
                    1).strip() if explanation_match else ""

                # Store refined query
                state["refined_query"] = refined_query

                # Store this interaction in conversation history
                state["conversation_history"].append({
                    "role": "assistant",
                    "content": f"I have enough information to proceed: {explanation}"
                })

                # Format response with clear sections
                response = (
                    f"RESULTS:\n"
                    f"I have enough information to proceed with the search.\n\n"
                    f"{explanation}\n\n"
                    f"NEXT_STEPS:\n"
                    f"1. Inform the user that I'm searching based on their query\n"
                    f"2. Call this tool again with the search stage\n\n"
                    f"NEXT_STAGE: SEARCH\n"
                    f"REFINED_QUERY: {refined_query}"
                )

            return [types.TextContent(type="text", text=response)]

        elif stage == "SEARCH":
            # Use the refined query from state
            refined_query = state.get("refined_query", query)

            # Perform search with refined query
            search_results = await perform_search_analysis(
                query=refined_query,
                pinecone_client=pinecone_client,
                cloudflare_uploader=cloudflare_uploader,
                request_id=request_id,
                inflight_requests=inflight_requests,
                model="openai/o3-mini",
                deepthink=False
            )

            # Extract text content
            search_content = "No relevant results found."
            if search_results and hasattr(search_results[0], 'text'):
                search_content = search_results[0].text

            # Store search results
            state["last_search_results"] = search_content

            # Store this interaction in conversation history
            state["conversation_history"].append({
                "role": "assistant",
                "content": f"Here are the search results for: {refined_query}"
            })

            # Format response with clear sections
            response = (
                f"RESULTS:\n"
                f"Here are the search results based on the query: {refined_query}\n\n"
                f"{search_content}\n\n"
                f"NEXT_STEPS:\n"
                f"1. Present these search results to the user\n"
                f"2. Ask the user to review the sources and confirm if they contain relevant information\n"
                f"3. IMPORTANT: Always call this tool again with stage=REFINE_SEARCH and include the user's feedback\n"
                f"   (Even if the user is satisfied, we need their confirmation before proceeding to the answer stage)\n\n"
                f"NEXT_STAGE: REFINE_SEARCH"
            )

            return [types.TextContent(type="text", text=response)]

        elif stage == "REFINE_SEARCH":
            # Get the last search results
            last_search_results = state.get(
                "last_search_results", "No previous search results.")

            # Check if user is satisfied with the sources
            user_satisfied = any(term in user_input.lower() for term in [
                                 "satisfied", "good", "yes", "helpful", "useful", "relevant", "proceed", "answer"])

            if user_satisfied:
                # User is satisfied with the sources, proceed to ANSWER
                # Store this interaction in conversation history
                state["conversation_history"].append({
                    "role": "assistant",
                    "content": "Thank you for confirming the sources. I'll now generate a comprehensive answer based on these sources."
                })

                # Format response to proceed to ANSWER
                response = (
                    f"RESULTS:\n"
                    f"The user has confirmed that the sources contain relevant information.\n\n"
                    f"NEXT_STEPS:\n"
                    f"1. Inform the user that you're generating an answer based on the confirmed sources\n"
                    f"2. Call this tool with stage=ANSWER\n\n"
                    f"NEXT_STAGE: ANSWER"
                )

                return [types.TextContent(type="text", text=response)]
            else:
                # User wants to refine the search
                # Refine the search based on user feedback
                refinement = await make_api_call(
                    search_refinement_prompt.format(
                        query=query,
                        search_results=last_search_results,
                        conversation_history=conversation_text,
                        user_feedback=user_input
                    ),
                    model="openai/o3-mini"
                )

                # Parse the refinement
                refined_query_match = re.search(r"REFINED_QUERY:(.*?)(?:EXPLANATION:|$)",
                                                refinement, re.DOTALL)
                explanation_match = re.search(
                    r"EXPLANATION:(.*?)$", refinement, re.DOTALL)

                refined_query = refined_query_match.group(
                    1).strip() if refined_query_match else query
                explanation = explanation_match.group(
                    1).strip() if explanation_match else ""

                # Store refined query
                state["refined_query"] = refined_query

                # Store this interaction in conversation history
                state["conversation_history"].append({
                    "role": "assistant",
                    "content": f"I've refined the search based on your feedback: {explanation}"
                })

                # Format response with clear sections
                response = (
                    f"RESULTS:\n"
                    f"I've refined the search based on your feedback.\n\n"
                    f"{explanation}\n\n"
                    f"NEXT_STEPS:\n"
                    f"1. Inform the user that I'm refining the search based on their feedback\n"
                    f"2. Call this tool again with the search stage to get new results\n\n"
                    f"NEXT_STAGE: SEARCH\n"
                    f"REFINED_QUERY: {refined_query}"
                )

                return [types.TextContent(type="text", text=response)]

        elif stage == "ANSWER":
            # Use the refined query from state
            refined_query = state.get("refined_query", query)

            # Get the last search results or perform a new search if needed
            if "last_search_results" in state and state["last_search_results"]:
                search_content = state["last_search_results"]
            else:
                # Perform search with refined query
                search_results = await perform_search_analysis(
                    query=refined_query,
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests,
                    model="openai/o3-mini",
                    deepthink=False
                )

                # Extract text content
                search_content = "No relevant results found."
                if search_results and hasattr(search_results[0], 'text'):
                    search_content = search_results[0].text

            # Generate final answer
            final_answer = await make_api_call(
                final_answer_prompt.format(
                    query=query,
                    conversation_history=conversation_text,
                    search_results=search_content
                ),
                model="openai/o3-mini"
            )

            # Store this interaction in conversation history
            state["conversation_history"].append({
                "role": "assistant",
                "content": final_answer
            })

            # Format response with clear sections
            response = (
                f"RESULTS:\n"
                f"{final_answer}\n\n"
                f"SOURCE_INFORMATION:\n"
                f"{search_content}\n\n"
                f"NEXT_STEPS:\n"
                f"1. Present the answer to the user\n"
                f"2. The search process is now complete\n\n"
                f"NEXT_STAGE: COMPLETE"
            )

            # Clean up state
            if request_id in deep_research.state:
                del deep_research.state[request_id]

            return [types.TextContent(type="text", text=response)]

        else:
            return [types.TextContent(type="text", text="Invalid stage specified. Please use 'CLARIFICATION', 'SEARCH', 'REFINE_SEARCH', or 'ANSWER'.")]

    except Exception as e:
        logger.error(f"Error in deep_research: {str(e)}")
        inflight_requests[request_id] = "error"
        raise


@log_cancellation
async def save_memory(
    memory_text: str,
    pinecone_client: PineconeManager,
    cloudflare_uploader: CloudflareUploader,
    request_id: str,
    inflight_requests: dict
) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Save a memory to Cloudflare and Pinecone"""
    try:
        inflight_requests[request_id] = "running"

        # Create temporary file with memory content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = Path(f"memory_{timestamp}.txt")
        temp_file.write_text(memory_text)

        try:
            # Upload to Cloudflare
            cloudflare_path, metadata = cloudflare_uploader.upload_document(
                str(temp_file), {})

            if not cloudflare_path:
                raise Exception("Failed to upload memory to Cloudflare")

            # Create embedding for the memory text (using same text as summary)
            embedding = pinecone_client.create_embedding(memory_text)

            # Upsert to Pinecone
            success = pinecone_client.upsert_vector(
                vector_id=f"memory_{timestamp}",
                vector_values=embedding,
                metadata={
                    "summary": memory_text,
                    "cloudflare_path": cloudflare_path
                }
            )

            if not success:
                raise Exception("Failed to save memory to Pinecone")

            inflight_requests[request_id] = "done"
            return [types.TextContent(type="text", text="Memory successfully saved.")]

        finally:
            # Clean up temp file
            temp_file.unlink(missing_ok=True)

    except Exception as e:
        logger.error(f"Error in save_memory: {str(e)}")
        inflight_requests[request_id] = "error"
        raise


def register_tools(server: Server, pinecone_client: PineconeManager, cloudflare_uploader: CloudflareUploader, inflight_requests: dict):
    @server.list_tools()
    @log_cancellation
    async def handle_list_tools() -> list[types.Tool]:
        return ServerTools

    @server.call_tool()
    @log_cancellation
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        try:
            request_id = arguments.get("__request_id__")
            logger.info(f"Calling tool: {name} for request {request_id}")

            if name == ToolName.QUICK_SEARCH:
                return await perform_search_analysis(
                    query=arguments.get("query"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests,
                    model="openai/o3-mini",
                    deepthink=False
                )
            elif name == ToolName.REMEMBER:
                return await save_memory(
                    memory_text=arguments.get("memory_text"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests
                )
            elif name == ToolName.DEEP_RESEARCH:
                return await deep_research(
                    query=arguments.get("query"),
                    # Default to CLARIFICATION if not provided
                    stage=arguments.get("stage", "CLARIFICATION"),
                    request_id=request_id,  # Always use the MCP request_id
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    inflight_requests=inflight_requests,
                    user_input=arguments.get("user_input", "")
                )
            else:
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}")
            raise


__all__ = [
    "register_tools",
]
