from langchain.chat_models import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.config.config import MODEL_NAME
from src.database.vector_store import VectorStore

PROMPT_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""

class ChatModel:
    def __init__(self):
        self.llm = Ollama(model=MODEL_NAME)
        self.vector_store = VectorStore()
        self.prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.get_retriever(),
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=True
        )
    
    def get_response(self, query):
        try:
            response = self.qa_chain({"query": query})
            return {
                "answer": response["result"],
                "sources": [doc.metadata for doc in response["source_documents"]]
            }
        except Exception as e:
            return {"error": str(e)}
