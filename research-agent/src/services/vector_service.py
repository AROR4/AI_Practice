from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_chroma import Chroma


class VectorService:

    def __init__(self):

        self.persist_directory = "vector_store"

        self.embedding_model = (
            HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )

    def build_vector_store(self):

        print("Loading documents...")

        loader = DirectoryLoader(
            "data/policies",
            glob="**/*.txt",
            loader_cls=TextLoader
        )

        documents = loader.load()

        print(
            f"Loaded {len(documents)} documents"
        )

        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
        )

        chunks = splitter.split_documents(
            documents
        )

        print(
            f"Created {len(chunks)} chunks"
        )

        Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory
        )

        print(
            "Vector database created"
        )

    def get_vector_store(self):

        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

    def search_documents(
        self,
        query: str,
        k: int = 3
    ):

        vector_store = self.get_vector_store()

        results = (
            vector_store.similarity_search(
                query=query,
                k=k
            )
        )

        return results