from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
import os


MODEL_NAME = "llama3"
BASE_DIR = "vector_db_dir"
EMBEDDING_MODEL = OllamaEmbeddings(model=MODEL_NAME)
EMB_DIMENSION = 4096
os.makedirs(BASE_DIR, exist_ok=True)


def get_user_index(user_id: int):
    return os.path.join(BASE_DIR, f"user_index_{user_id}")


def load_or_create_index(user_id: int):
    path = get_user_index(user_id)
    if os.path.exists(path):
        return FAISS.load_local(
            path, EMBEDDING_MODEL, allow_dangerous_deserialization=True
        )
    else:
        index = faiss.IndexFlatL2(EMB_DIMENSION)
        return FAISS(
            EMBEDDING_MODEL.embed_query,
            index,
            docstore=InMemoryDocstore({}),
            index_to_docstore_id={},
        )


def save_index(user_id: int, faiss_index: FAISS):
    path = get_user_index(user_id)
    faiss_index.save_local(path)


def add_document(user_id: int, doc: Document):
    faiss_index = load_or_create_index(user_id)
    faiss_index.add_documents([doc])
    save_index(user_id, faiss_index)


def query_documents(faiss_index: FAISS, query: str, k: int = 3):
    docs = faiss_index.similarity_search(query, k=k)
    return docs


if __name__ == "__main__":
    DUMMY_ID = 10_000
    index = load_or_create_index(DUMMY_ID)
    save_index(DUMMY_ID, index)
