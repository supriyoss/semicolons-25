
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize Pinecone and SentenceTransformer
pc = Pinecone(api_key='pcsk_42PvD3_GYZJ5WrR3jWcCwt7QLPNurtN2QcpJFCozvHvqRfDhH2mpjNnwmwRxRs26QCH8HK')  # Replace with your Pinecone API key
model = SentenceTransformer("all-MiniLM-L6-v2")
# Connect to the Pinecone index
index_name = "ocr-embeddings"
index = pc.Index(index_name)
# Example query text
query_text = "What is the patient name?"
# Convert query text to an embedding (vector) using SentenceTransformer
query_vector = model.encode(query_text).tolist()  # Encoding the query text
# Perform a vector search in Pinecone
results = index.query(
    vector=query_vector,  # The query vector
    top_k=5,  # Number of results to retrieve
    include_values=True,  # Option to include the actual vectors with the results
    include_metadata=True  # Option to include any metadata associated with vectors (if you added metadata)
)

# Output the results
print("Top search results:")
for match in results['matches']:
    print(f"ID: {match['id']}, Score: {match['score']}")
    if 'metadata' in match:
        print(f"Metadata: {match['metadata']}")  # If you have metadata, it will be printed here
    print()

