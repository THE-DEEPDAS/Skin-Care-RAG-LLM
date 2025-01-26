
# RAG-Based LLM Chatbot for Skincare Clinic

This project focuses on implementing a **Retrieval-Augmented Generation (RAG)** based chatbot tailored for a skincare clinic. The chatbot provides two key functionalities:
1. **Clinic Appointment Booking**: Allows users to book appointments with the clinic. 
2. **Skincare Q&A**: Answers queries related to skincare by retrieving information from a PDF knowledge base.

---

## Workflow

### **1. User Query Input**
The user interacts with the chatbot, submitting a query such as:
*"What treatments are available for sensitive skin?"*

### **2. Retriever**
The query is passed to a **Retriever** that identifies the most relevant information from a knowledge base by matching embeddings (vector representations of data).

### **3. Vector Database**
A **free vector database** (like FAISS or ChromaDB) stores pre-computed embeddings of the documents (e.g., FAQs, treatment descriptions, skincare advice). The retriever fetches chunks most similar to the user query.

### **4. Document Chunk Embeddings**
The fetched document chunks are added as context to the query, ensuring the LLM generates responses grounded in the knowledge base.

### **5. LLM (Large Language Model)**
The **LLM** (like LLaMA 2 or GPT-4) takes the query and retrieved context as input. It processes the combined data to generate an accurate, context-aware, and user-friendly response.

### **6. Final Response Output**
The chatbot displays the response to the user, answering their query effectively.

---

## Tool Options for Implementation

### **1. Tools like LLMWare or Anything-LLM**
- **LLMWare:** 
   - Ideal for simple deployments with built-in RAG pipelines.
   - Offers ease of use and abstraction over RAG workflows.
   - Suitable for small to medium-scale projects without extensive customization.

- **Anything-LLM:**
   - A solid choice for open-source, scalable chatbot projects.
   - Includes pre-built integrations and focuses on flexibility and performance.
   - Great for experimental or production-grade projects.

### **2. Custom Implementation Using LangChain**
If you prefer full control and extensibility, the **custom approach** using LangChain, Ollama (to host LLaMA 2), and free vector databases like FAISS or ChromaDB is more beneficial. Here’s why:
- **Customization:** You can design retrieval, memory, and context-handling workflows to suit your clinic's needs.
- **Cost-Efficiency:** Free tools and self-hosted LLMs save on API costs.
- **Transparency:** Full visibility into how embeddings, retrieval, and generation work.

---

## Implementation with LangChain, LLaMA 2, and ChromaDB

### **Step 1: Install Dependencies**
```bash
pip install langchain chromadb sentence-transformers ollama
```

### **Step 2: Setup LLaMA 2 Using Ollama**
- Install Ollama and run LLaMA 2 locally:  
  [Ollama Documentation](https://www.ollama.com/docs).

### **Step 3: Code the Workflow**
```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import Ollama
from langchain.prompts import PromptTemplate

# 1. Load embeddings and initialize vector database
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="db", embedding_function=embedding_model)

# 2. Create a retriever from the vector database
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 3. Initialize LLaMA 2 via Ollama
llm = Ollama(model="llama2-7b")

# 4. Create Retrieval-Augmented QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True
)

# 5. Sample query
query = "What are the treatments for acne?"
response = qa_chain.run(query)
print(response)
```

---

## Customizing the Appointment Booking

### **Steps to Integrate Appointment Booking:**
1. **Create a Booking Endpoint**:
   - Build a simple API using Flask, FastAPI, or Node.js to handle appointment data (name, date, etc.).
   - Store the appointments in a database or a calendar API (e.g., Google Calendar).

2. **Add Appointment Logic in Anything-LLM**:
   - Define a **custom handler** in Anything-LLM to redirect appointment-related queries to the booking API.
   - Example trigger phrases:
     - "I want to book an appointment."
     - "Can I schedule a visit next week?"

3. **Sample Code for the Booking Handler:**
   Create an API endpoint (e.g., `/book-appointment`):
   ```python
   from flask import Flask, request, jsonify

   app = Flask(__name__)

   # In-memory database for demo purposes
   appointments = []

   @app.route('/book-appointment', methods=['POST'])
   def book_appointment():
       data = request.json
       name = data.get('name')
       date = data.get('date')
       time = data.get('time')
       contact = data.get('contact')

       if not all([name, date, time, contact]):
           return jsonify({"error": "Missing required fields"}), 400

       # Add the appointment to the database
       appointments.append({"name": name, "date": date, "time": time, "contact": contact})
       return jsonify({"message": "Appointment booked successfully!"})

   if __name__ == "__main__":
       app.run(port=5000)
   ```

4. **Connect to Anything-LLM**:
   - Modify the custom handler to make API calls to the `/book-appointment` endpoint.
   - Example:
     ```javascript
     const axios = require('axios');

     module.exports = async function handleAppointment(query) {
         if (query.includes('appointment')) {
             const response = await axios.post('http://localhost:5000/book-appointment', {
                 name: 'User Name', 
                 date: '2025-01-30', 
                 time: '10:00 AM', 
                 contact: 'user@example.com'
             });

             return `Your appointment is booked: ${response.data.message}`;
         }
     };
     ```

---

## Future Enhancements
1. **Multi-User Support**: Allow multiple users to interact with the chatbot simultaneously.
2. **Live Availability Check**: Sync with Google Calendar or similar tools to show real-time appointment availability.
3. **Advanced Q&A Features**: Integrate symptom-matching logic or specialized medical advice models.

---

## Advantages of This Setup
1. **Effortless PDF Integration**: Anything-LLM handles document embedding and indexing.
2. **Custom Task Flexibility**: Appointment booking is easily implemented with custom handlers.
3. **Cost Efficiency**: Using free tools like FAISS for vector storage and Ollama for hosting LLaMA 2 reduces costs.

Let me know if you have questions or need help with the setup!
