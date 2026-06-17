import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline

model = SentenceTransformer('all-MiniLM-L6-v2')

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="docs")

st.title("RAG Chatbot")

query = st.text_input("Ask Question")

if query:

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = "\n".join(results["documents"][0])

    prompt = f"""
    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = generator(
    prompt,
    max_new_tokens=100
    )

    st.write(response[0]["generated_text"])
