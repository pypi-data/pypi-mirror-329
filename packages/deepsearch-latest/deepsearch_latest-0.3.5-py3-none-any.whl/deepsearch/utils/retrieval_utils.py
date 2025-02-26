from typing import List, Dict, Any, Tuple
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.text_chunking import (DocumentChunk, chunk_document, create_rerank_batches,
                                            plot_score_distributions)
from collections import defaultdict
import asyncio


def retrieve_and_analyze_documents(query: str, min_normalized_score: float = 0.5) -> Tuple[List[Dict[str, Any]], Dict[str, List[float]], Dict[str, List[float]], Dict[str, str]]:
    """
    Retrieve documents, chunk them, and perform detailed reranking analysis.
    Filter chunks based on normalized scores.

    Returns:
        Tuple containing:
        - List of retrieved documents with their initial scores
        - Dictionary of raw scores by document
        - Dictionary of normalized scores by document
        - Dictionary mapping document paths to their full text
    """
    try:
        # Initialize managers
        pinecone = PineconeManager()
        uploader = CloudflareUploader()

        # Initial search (synchronous operation)
        search_results = pinecone.search_documents(
            query, min_normalized_score=0.2)

        # Process documents and create chunks
        all_chunks = []
        document_texts = {}

        # This is the only part that should be async - we can make a helper function
        document_texts = asyncio.run(
            fetch_all_documents(search_results, uploader))

        for result in search_results:
            if document_text := document_texts.get(result['cloudflare_path']):
                chunks = chunk_document(
                    document_text, result['cloudflare_path'])
                all_chunks.extend(chunks)

        # Create batches for reranking
        chunk_batches = create_rerank_batches(all_chunks)

        # Rerank all chunks
        raw_scores_by_doc = defaultdict(list)
        normalized_scores_by_doc = defaultdict(list)
        filtered_chunks = []  # Store chunks that meet the normalized score threshold

        for batch in chunk_batches:
            chunk_texts = [chunk.text for chunk in batch]
            reranked = pinecone.pc.inference.rerank(
                model="cohere-rerank-3.5",
                query=query,
                documents=chunk_texts,
                top_n=len(chunk_texts),
                return_documents=True
            )

            # Get max score for normalization
            max_score = max((r.score for r in reranked.data), default=1.0)

            # Process scores and filter by normalized score
            for chunk, result in zip(batch, reranked.data):
                normalized_score = result.score / max_score
                if normalized_score >= min_normalized_score:  # Only include chunks above threshold
                    raw_scores_by_doc[chunk.source_path].append(result.score)
                    normalized_scores_by_doc[chunk.source_path].append(
                        normalized_score)
                    filtered_chunks.append({
                        'chunk': chunk.text,
                        'source': chunk.source_path,
                        'raw_score': result.score,
                        'normalized_score': normalized_score
                    })

        # Sort filtered chunks by normalized score
        filtered_chunks.sort(key=lambda x: x['normalized_score'], reverse=True)

        # Get relevant document texts
        relevant_docs = {path: document_texts[path]
                         for path in raw_scores_by_doc.keys()
                         if path in document_texts}

        # Return only documents that had chunks meeting the threshold
        filtered_results = [
            r for r in search_results if r['cloudflare_path'] in raw_scores_by_doc]

        return filtered_results, raw_scores_by_doc, normalized_scores_by_doc, relevant_docs

    except Exception as e:
        print(f"Error in document retrieval and analysis: {str(e)}")
        return [], {}, {}, {}


async def fetch_all_documents(search_results, uploader):
    """Helper function to fetch documents concurrently"""
    tasks = [
        uploader._fetch_document_text(result['cloudflare_path'])
        for result in search_results
    ]
    results = await asyncio.gather(*tasks)
    return {
        result['cloudflare_path']: text
        for result, text in zip(search_results, results)
        if text
    }
