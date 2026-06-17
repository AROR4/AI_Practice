from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks

data_folder = "data"

for file in os.listdir(data_folder):

    if file.endswith(".pdf"):

        text = extract_text(os.path.join(data_folder, file))
        chunks = chunk_text(text)

        embeddings = model.encode(chunks).tolist()

        ids = [f"{file}_{i}" for i in range(len(chunks))]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks
        )

print("Embedding completed!")