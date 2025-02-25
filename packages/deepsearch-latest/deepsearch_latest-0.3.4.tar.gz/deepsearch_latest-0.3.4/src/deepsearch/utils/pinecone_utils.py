import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger("deepsearch-mcp")


class PineconeManager:
    def __init__(self):
        """Initialize Pinecone with API key for both vector operations and reranking."""
        api_key = os.getenv('PINECONE_API_KEY')
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(os.getenv('PINECONE_INDEX_NAME'))

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text string."""
        embeddings = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[text],
            parameters={"input_type": "passage", "truncate": "END"}
        )
        # The embeddings object returns a list of dictionaries with 'values' key
        return embeddings[0]['values']

    def upsert_vector(self,
                      vector_id: str,
                      vector_values: List[float],
                      metadata: Dict[str, Any],
                      namespace: str = "default") -> bool:
        """Upsert a single vector to Pinecone."""
        try:
            # Format records according to Pinecone documentation
            records = [{
                "id": vector_id,
                "values": vector_values,
                "metadata": metadata
            }]

            self.index.upsert(vectors=records, namespace=namespace)
            return True
        except Exception as e:
            logger.error(f"Error upserting vector: {str(e)}")
            return False

    def query_vectors(self,
                      query_vector: List[float],
                      top_k: int = 200,
                      namespace: str = "default",
                      filter_dict: Dict = None) -> Optional[Dict]:
        """Query vectors from Pinecone."""
        try:
            return self.index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=namespace,
                filter=filter_dict,
                include_metadata=True  # Always include metadata for search_documents
            )
        except Exception as e:
            logger.error(f"Error querying vectors: {str(e)}")
            return None

    def search_documents(self, query: str, min_normalized_score: float = 0.2) -> List[Dict[str, Any]]:
        """
        Search documents using a two-stage retrieval process with score normalization:
        1. Get top-k semantically similar documents using vector search
        2. Rerank results using Pinecone's reranking model
        3. Normalize scores relative to the highest score

        Args:
            query (str): The search query
            min_normalized_score (float): Minimum normalized similarity score threshold (default: 0.5)

        Returns:
            List[Dict[str, Any]]: List of documents with their scores and cloudflare paths
        """
        try:
            # Create query embedding
            query_embedding = self.create_embedding(query)

            # Get top-k results from vector search
            results = self.query_vectors(
                query_vector=query_embedding,
                top_k=200  # Get more initial results since we'll filter
            )

            if not results or 'matches' not in results:
                return []

            # Get max score for normalization of vector search scores
            max_vector_score = max(
                (match.score for match in results['matches']), default=1.0)

            # Extract document summaries and keep track of cloudflare paths, filtering by normalized score
            documents = []
            doc_paths = {}

            for idx, match in enumerate(results['matches']):
                normalized_score = match.score / max_vector_score
                if normalized_score >= min_normalized_score:
                    summary = match['metadata'].get('summary')
                    cloudflare_path = match['metadata'].get('cloudflare_path')
                    if summary and cloudflare_path:
                        documents.append(summary)
                        doc_paths[str(idx)] = cloudflare_path

            if not documents:
                return []

            # Rerank results using Pinecone's reranking capability
            reranked = self.pc.inference.rerank(
                model="cohere-rerank-3.5",
                query=query,
                documents=documents,
                top_n=len(documents),
                return_documents=True
            )

            # Get the maximum score for normalization
            max_score = max((r.score for r in reranked.data), default=1.0)

            # Format results with both raw and normalized scores
            filtered_results = []
            for result in reranked.data:
                # Calculate normalized score
                normalized_score = result.score / max_score if max_score > 0 else 0

                if normalized_score >= min_normalized_score:
                    doc_idx = str(documents.index(result.document.text))
                    filtered_results.append({
                        'raw_score': result.score,
                        'normalized_score': normalized_score,
                        'cloudflare_path': doc_paths[doc_idx],
                        'summary': result.document.text
                    })

            return filtered_results

        except Exception as e:
            logger.error(f"Error in search_documents: {str(e)}")
            return []
