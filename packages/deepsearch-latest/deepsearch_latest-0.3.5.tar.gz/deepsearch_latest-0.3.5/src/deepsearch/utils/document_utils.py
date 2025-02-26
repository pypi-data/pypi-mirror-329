from deepsearch.utils.openrouter_utils import make_api_call
from deepsearch.utils.prompts import document_summary_prompt
import os


async def create_document_summary(document_path: str, document_content: str) -> str:
    """
    Create a summary for a document using AI.

    Args:
        document_path (str): Path to the document (used for the name in the prompt)
        document_content (str): The content of the document to summarize

    Returns:
        str: The generated summary
    """
    formatted_prompt = document_summary_prompt.format(
        document_name=os.path.basename(document_path),
        document=document_content
    )
    return await make_api_call(formatted_prompt)
