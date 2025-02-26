import asyncio
from pathlib import Path
from typing import Tuple
from deepsearch.utils.file_converter import convert_directory_to_text
from deepsearch.utils.openrouter_utils import make_api_call
from deepsearch.utils.prompts import document_summary_prompt
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.document_utils import create_document_summary


async def process_document(txt_path: str) -> Tuple[str, str]:
    """Get summary for a document and return both summary and file content."""
    # Read the document
    with open(txt_path, 'r') as f:
        document = f.read()

    # Get document summary using the new utility function
    summary = await create_document_summary(txt_path, document)

    return summary, document


async def process_directory(input_dir: str) -> None:
    """Process all documents in a directory."""
    # Initialize managers
    uploader = CloudflareUploader()
    pinecone = PineconeManager()

    # Convert all files to txt
    temp_dir = Path(input_dir) / 'temp_txt'
    converted_files = await convert_directory_to_text(input_dir, str(temp_dir))

    for txt_path in converted_files:
        try:
            # Get summary and content
            summary, document_text = await process_document(str(txt_path))

            # Upload to Cloudflare
            cloudflare_path, _ = uploader.upload_document(str(txt_path), {})

            if not cloudflare_path:
                print(f"Failed to upload {txt_path} to Cloudflare")
                continue

            # Create embedding for the summary
            embedding = pinecone.create_embedding(summary)

            # Upsert to Pinecone
            success = pinecone.upsert_vector(
                vector_id=str(txt_path.stem),
                vector_values=embedding,
                metadata={
                    "summary": summary,
                    "cloudflare_path": cloudflare_path
                }
            )

            if success:
                print(f"Successfully processed {txt_path.name}")
            else:
                print(f"Failed to upsert vector for {txt_path.name}")

        except Exception as e:
            print(f"Error processing {txt_path}: {str(e)}")
        finally:
            # Clean up temp txt file
            txt_path.unlink(missing_ok=True)

    # Clean up temp directory if empty
    try:
        temp_dir.rmdir()
    except:
        pass

if __name__ == "__main__":
    input_directory = "test_documents"
    asyncio.run(process_directory(input_directory))
