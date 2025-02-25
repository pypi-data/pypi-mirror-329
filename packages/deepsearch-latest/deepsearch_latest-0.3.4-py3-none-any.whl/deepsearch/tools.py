import logging
from typing import Sequence, Union
from enum import Enum
import mcp.types as types
from mcp.server import Server
from deepsearch.utils.search_utils import async_fetch_all_documents, async_process_documents_with_openrouter
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.async_utils import log_cancellation
from datetime import datetime
from pathlib import Path
from deepsearch.utils.openrouter_utils import perform_deep_analysis

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepsearch-mcp")


class ToolName(str, Enum):
    PERFORM_ANALYSIS = "perform-analysis"
    DEEPTHINK = "deepthink"
    REMEMBER = "remember"


ServerTools = [
    types.Tool(
        name=ToolName.PERFORM_ANALYSIS,
        description="Passes the user query and uses it to search across the database documents.",
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
        name=ToolName.DEEPTHINK,
        description="Performs an iterative deep analysis of the search results. If the initial search doesn't yield complete information to answer the query, it will automatically generate and execute follow-up searches to fill in missing information. Each iteration includes detailed calculations, cross-referencing across sources, and synthesis of information. The process continues until either a complete answer is found or it's determined that the information is not available in the knowledge base.",
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

            if name == ToolName.PERFORM_ANALYSIS:
                return await perform_search_analysis(
                    query=arguments.get("query"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests,
                    model="openai/o3-mini",
                    deepthink=False
                )
            elif name == ToolName.DEEPTHINK:
                search_results = await perform_search_analysis(
                    query=arguments.get("query"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests,
                    model="openai/o1",
                    deepthink=True
                )

                if not search_results:
                    return [types.TextContent(
                        type="text",
                        text="No relevant documents found in the knowledge base for your query. Please try reformulating your question or check if this information exists in the database."
                    )]

                # Extract the text content from the TextContent object
                search_content = search_results[0].text

                # Perform deep analysis using openai/o1
                deep_analysis = await perform_deep_analysis(
                    query=arguments.get("query"),
                    extracted_info=search_content,
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests
                )

                # Format the complete response
                complete_response = (
                    f"=== SEARCH RESULTS ===\n{search_content}\n\n"
                    f"=== DEEP ANALYSIS ===\n{deep_analysis}"
                )

                # Return the complete analysis as a TextContent object
                return [types.TextContent(type="text", text=complete_response)]
            elif name == ToolName.REMEMBER:
                return await save_memory(
                    memory_text=arguments.get("memory_text"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests
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
