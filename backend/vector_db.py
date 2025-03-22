import pinecone
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Pinecone setup
#PINECONE_API_KEY = "pcsk_42PvD3_GYZJ5WrR3jWcCwt7QLPNurtN2QcpJFCozvHvqRfDhH2mpjNnwmwRxRs26QCH8HK"
PINECONE_ENV = "us-east-1"

pc = Pinecone(api_key='pcsk_42PvD3_GYZJ5WrR3jWcCwt7QLPNurtN2QcpJFCozvHvqRfDhH2mpjNnwmwRxRs26QCH8HK')
# api_key=os.environ.get("PINECONE_API_KEY")
index_name = "ocr-embeddings"

if index_name not in pc.list_indexes().names():
    pinecone.create_index(name=index_name, dimension=384)  # Model has a 384-dimensional output

index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')


def get_text_embedding(text):
    """Generate embeddings using the SentenceTransformer model."""
    return model.encode(text).tolist()


def save_text_embedding(unique_id, extracted_text):
    """Save extracted text and its embedding to Pinecone."""
    embedding = get_text_embedding(extracted_text)
    sanitized_id = unique_id.replace("\\", "/")  # Handle Windows file paths

    index.upsert([(sanitized_id, embedding, {"text": extracted_text})])
    print(f"Saved embedding for: {sanitized_id}")
