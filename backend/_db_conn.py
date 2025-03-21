"""
pip install fastapi uvicorn redis redisvl numpy pytesseract pillow sentence-transformers pdf2image


"""
import redis
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.schema import TagField, VectorField, TextField
from fastapi import FastAPI, UploadFile, File, Form
import os
import uuid

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim vector

# FastAPI app
app = FastAPI(title="PDF OCR & Vector Search API")

# Redis Config
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
INDEX_NAME = "ocr_pdf_vector_index"

# Connect to Redis
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=False)

# Define Redis Schema
schema = [
    TagField(name="id"),  # Unique document ID
    TextField(name="text"),  # Extracted OCR text
    VectorField(name="embedding", dims=384, algorithm="HNSW"),  # Vector embedding
]

# Initialize Redis Vector Index
index = SearchIndex(client=client, name=INDEX_NAME, schema=schema)


def ensure_index():
    """Ensures the Redis vector index exists."""
    if not index.exists():
        print("Creating Redis vector index...")
        index.create()
        print("Index created successfully.")
    else:
        print("Index already exists.")


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using OCR."""
    try:
        images = convert_from_path(pdf_path)  # Convert PDF pages to images
        ocr_text = []

        for img in images:
            text = pytesseract.image_to_string(img)  # Extract text from each page
            ocr_text.append(text.strip())

        return "\n".join(ocr_text)  # Combine text from all pages

    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


def generate_embedding(text):
    """Generates a real vector embedding using Sentence-Transformers."""
    return embedding_model.encode(text).tolist()


def store_pdf_ocr_data(doc_id, text):
    """Stores OCR text & embeddings in Redis."""
    embedding = generate_embedding(text)

    data = {
        "id": doc_id,
        "text": text,
        "embedding": embedding
    }

    index.upsert(doc_id, data)
    print(f"Stored PDF {doc_id} in Redis.")


def search_similar_documents(query_text, top_n=5):
    """Searches for similar OCR documents using vector similarity."""
    query_vector = generate_embedding(query_text)

    query = VectorQuery(
        vector=query_vector,
        vector_field="embedding",
        return_fields=["id", "text"],
        num_results=top_n
    )

    results = index.query(query)
    return results


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """API endpoint to upload a PDF & store OCR data in Redis."""
    try:
        file_path = f"uploads/{uuid.uuid4()}.pdf"
        os.makedirs("uploads", exist_ok=True)

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        text = extract_text_from_pdf(file_path)
        if not text:
            return {"error": "No text extracted"}

        # Store in Redis
        doc_id = str(uuid.uuid4())
        store_pdf_ocr_data(doc_id, text)

        return {"message": "PDF processed successfully", "document_id": doc_id}

    except Exception as e:
        return {"error": str(e)}


@app.get("/search/")
async def search(query: str, top_n: int = 5):
    """API endpoint to search for similar documents."""
    results = search_similar_documents(query, top_n)
    return results


if __name__ == "__main__":
    ensure_index()
