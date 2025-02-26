import logging
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import importlib.metadata
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from .tools import register_tools
from deepsearch.utils.async_utils import log_cancellation
from .intercepting_stream import InterceptingStream

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepsearch-mcp")

# Initialize server
server = Server("deepsearch-mcp")

# Initialize global clients
pinecone_client = None
cloudflare_uploader = None

# Track request statuses
inflight_requests = {}


@server.progress_notification()
async def handle_progress_notification(progress_token: str | int, progress: float, total: float | None):
    """Handle progress notifications from the client."""
    try:
        request_id = str(progress_token)
        if request_id in inflight_requests:
            logger.info(
                f"Received progress update for request {request_id}: {progress}/{total}")
            if progress < 0:  # Use negative progress as a cancellation signal
                logger.info(f"Cancelling request {request_id}")
                inflight_requests[request_id] = "cancelled"
        else:
            logger.warning(
                f"Received progress for unknown request {request_id}")
    except Exception as e:
        logger.error(f"Error handling progress notification: {str(e)}")


@log_cancellation
async def main():
    """Start the MCP server with proper initialization."""
    try:
        logger.info("Starting Deepsearch MCP server")

        global pinecone_client, cloudflare_uploader
        pinecone_client = PineconeManager()
        cloudflare_uploader = CloudflareUploader()
        register_tools(server, pinecone_client,
                       cloudflare_uploader, inflight_requests)

        async with mcp.server.stdio.stdio_server() as (base_read_stream, write_stream):
            # Wrap the base_read_stream with our custom interceptor
            intercepted_read_stream = InterceptingStream(base_read_stream)

            await server.run(
                intercepted_read_stream,
                write_stream,
                InitializationOptions(
                    server_name="deepsearch",
                    server_version=importlib.metadata.version(
                        "deepsearch-latest"),
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(
                            resources_changed=True,
                            prompts_changed=False,
                            tools_changed=False
                        ),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise
