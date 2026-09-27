import os

from dotenv import load_dotenv
from google import genai

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import TextLoader


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


client = genai.Client(
    api_key=api_key
)


# ---------------------------------------------------------
# Gemini Embeddings
# ---------------------------------------------------------

class GeminiEmbeddings(Embeddings):

    def embed_documents(self, texts):

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts
        )

        return [
            embedding.values
            for embedding in result.embeddings
        ]

    def embed_query(self, text):

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return result.embeddings[0].values


# ---------------------------------------------------------
# Load Laptop Data
# ---------------------------------------------------------

documents = []

files = [
    "data/laptops.txt",
    "data/processors.txt",
    "data/reviews.txt"
]


for file in files:

    loader = TextLoader(
        file,
        encoding="utf-8"
    )

    documents.extend(
        loader.load()
    )


print(
    "Loaded documents:",
    len(documents)
)


# ---------------------------------------------------------
# Create Embeddings
# ---------------------------------------------------------

embeddings = GeminiEmbeddings()


# ---------------------------------------------------------
# Create FAISS Vector Store
# ---------------------------------------------------------

vector_store = FAISS.from_documents(
    documents,
    embeddings
)


# ---------------------------------------------------------
# Save Vector Store
# ---------------------------------------------------------

vector_store.save_local(
    "faiss_index"
)


print(
    "FAISS vector store created successfully!"
)