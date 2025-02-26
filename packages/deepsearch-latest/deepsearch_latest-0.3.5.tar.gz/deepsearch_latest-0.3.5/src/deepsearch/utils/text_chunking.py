import tiktoken
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    text: str
    source_path: str
    chunk_index: int
    token_count: int


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Count tokens in text using tiktoken."""
    encoder = tiktoken.get_encoding(model)
    return len(encoder.encode(text))


def chunk_document(text: str, source_path: str, chunk_size: int = 500, overlap: int = 50) -> List[DocumentChunk]:
    """
    Split document into chunks with overlap.

    Args:
        text (str): Text to chunk
        source_path (str): Source file path
        chunk_size (int): Target size of each chunk in tokens
        overlap (int): Number of tokens to overlap between chunks

    Returns:
        List[DocumentChunk]: List of document chunks
    """
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    chunks = []
    chunk_index = 0

    # Calculate step size (chunk_size - overlap)
    step_size = chunk_size - overlap

    # Create chunks with overlap
    for i in range(0, len(tokens), step_size):
        # Get chunk tokens (including overlap)
        chunk_tokens = tokens[i:i + chunk_size]

        if len(chunk_tokens) < 10:  # Skip very small final chunks
            continue

        # Decode chunk tokens back to text
        chunk_text = encoder.decode(chunk_tokens)

        chunks.append(DocumentChunk(
            text=chunk_text,
            source_path=source_path,
            chunk_index=chunk_index,
            token_count=len(chunk_tokens)
        ))
        chunk_index += 1

    return chunks


def create_rerank_batches(chunks: List[DocumentChunk], max_batch_tokens: int = 38000) -> List[List[DocumentChunk]]:
    """Create batches of chunks that fit within token limits."""
    batches = []
    current_batch = []
    current_batch_tokens = 0

    for chunk in chunks:
        if current_batch_tokens + chunk.token_count > max_batch_tokens:
            if current_batch:  # Add current batch if it exists
                batches.append(current_batch)
            current_batch = [chunk]
            current_batch_tokens = chunk.token_count
        else:
            current_batch.append(chunk)
            current_batch_tokens += chunk.token_count

    if current_batch:  # Add final batch if it exists
        batches.append(current_batch)

    return batches


def plot_score_distributions(scores_by_doc: Dict[str, List[float]], score_type: str):
    """Plot histogram of scores for each document."""
    plt.figure(figsize=(12, 6))

    # Create a color map for different documents
    colors = plt.cm.rainbow(np.linspace(0, 1, len(scores_by_doc)))

    for (doc_path, scores), color in zip(scores_by_doc.items(), colors):
        plt.hist(scores, alpha=0.5, label=f'Doc: {doc_path.split("/")[-1]}',
                 bins=20, color=color)

    plt.title(f'Distribution of {score_type} Scores Across Document Chunks')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save and close instead of showing
    plt.savefig(f'test_output/{score_type.lower()}_score_distribution.png')
    plt.close()
