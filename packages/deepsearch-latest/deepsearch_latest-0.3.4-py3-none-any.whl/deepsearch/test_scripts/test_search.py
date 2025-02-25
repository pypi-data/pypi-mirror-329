import asyncio
import os
from pathlib import Path
from deepsearch.utils.search_utils import perform_search_analysis
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.text_chunking import plot_score_distributions
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Load environment variables
load_dotenv()


async def main(
    query: str,
    output_dir: str = "test_output"
):
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Initialize clients
    pinecone_client = PineconeManager()
    cloudflare_uploader = CloudflareUploader()

    print(f"\nStarting search with query: {query}")
    print("="*80)

    results = await perform_search_analysis(
        query=query,
        pinecone_client=pinecone_client,
        cloudflare_uploader=cloudflare_uploader
    )

    # Print results
    if not results:
        print("\nNo results found.")
        return

    # Save results to a text file
    results_file = Path(output_dir) / f'search_results_{query[:30]}.txt'
    with open(results_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(f"\nSource: {result['source']}\n")
            f.write(f"Score: {result['score']:.3f}\n")
            f.write("Extracted Information:\n")
            f.write(result['extracted_info'])
            f.write("\n" + "="*80 + "\n")

    print(f"\nSearch results saved to: {results_file}")

    # Collect scores for plotting
    scores_by_doc = defaultdict(list)
    for result in results:
        scores_by_doc[result['source']].append(result['score'])

    # Plot score distribution
    plt.figure(figsize=(12, 6))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(scores_by_doc)))

    for (doc_path, scores), color in zip(scores_by_doc.items(), colors):
        plt.hist(scores, alpha=0.5, label=f'Doc: {os.path.basename(doc_path)}',
                 bins=20, color=color)

    plt.title('Distribution of Search Scores Across Documents')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save plot
    plot_path = Path(output_dir) / \
        f'search_scores_distribution_{query[:30]}.png'
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    print(f"\nScore distribution plot saved to: {plot_path}")


if __name__ == "__main__":
    # Test queries
    queries = [
        "What is the cost of sucrose per batch according to the techno economic model?",
        "What was the carbon feed rate at the beginning, and at the end of the run? On a grams of sucrose / L hr basis at the October sucrose run at Laurus Bio."
    ]

    # Run each query
    for query in queries:
        asyncio.run(main(query))
        print("\nScript finished!")
        print("\n" + "="*100 + "\n")
