from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from src.config.config import VECTOR_DB_PATH, EMBEDDING_MODEL

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
    
    def get_retriever(self, k=5):
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
