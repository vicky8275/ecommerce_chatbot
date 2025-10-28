# E-Commerce Chatbot Technology Education

This document explains all the key terms, terminologies, tools, and technologies used in this E-Commerce Chatbot project.

## 🏗️ **Core Architecture & Technologies**

### **1. FastAPI**
- **What it is**: A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Why used**:
  - High performance (one of the fastest Python frameworks)
  - Automatic API documentation generation
  - Built-in support for async operations
  - Easy to use and learn
- **Key features in our project**:
  - Serves the web interface at `/` endpoint
  - Handles chat requests at `/chat` endpoint
  - Provides health check at `/health`
  - Uses Pydantic for data validation

### **2. Ollama**
- **What it is**: A tool for running large language models (LLMs) locally on your machine.
- **Why used**:
  - No API costs (runs locally)
  - Privacy-focused (data stays on your machine)
  - Supports multiple models like llama3, phi3, etc.
- **How it works**:
  - Downloads and runs AI models locally
  - Provides REST API at `http://localhost:11434`
  - Our chatbot calls Ollama's `/api/generate` endpoint

### **3. FAISS (Facebook AI Similarity Search)**
- **What it is**: A library for efficient similarity search and clustering of dense vectors.
- **Why used**:
  - Fast vector similarity search for RAG
  - Handles high-dimensional vectors efficiently
  - Scales well with large datasets
- **How it works in our project**:
  - Stores embeddings of FAQ documents
  - Performs nearest neighbor search for user queries
  - Returns most relevant documents for context

### **4. Sentence Transformers**
- **What it is**: A Python framework for state-of-the-art sentence, text, and image embeddings.
- **Why used**: Converts text into numerical vectors (embeddings) that capture semantic meaning.
- **Key model**: `all-MiniLM-L6-v2` - creates 384-dimensional vectors from text.
- **How it works**:
  - Input: Text → Output: Vector representation
  - Similar texts have similar vectors
  - Used for both document indexing and query encoding

## 🤖 **AI/ML Concepts**

### **5. Retrieval-Augmented Generation (RAG)**
- **What it is**: A technique that combines information retrieval with generative AI.
- **Why it's powerful**:
  - Provides factual, up-to-date information
  - Reduces hallucinations in AI responses
  - More accurate than pure generative models
- **How it works in our chatbot**:
  1. User query → Convert to embedding
  2. Search FAISS index for similar documents
  3. Use retrieved docs as context for LLM
  4. Generate response with context

### **6. Embeddings**
- **What they are**: Numerical representations of text in vector space.
- **Why important**:
  - Capture semantic meaning of text
  - Enable mathematical similarity comparisons
  - Power modern NLP applications
- **Example**: "cat" and "kitten" have similar embeddings, "cat" and "car" have different ones.

### **7. Vector Database/Index**
- **What it is**: A database optimized for storing and searching high-dimensional vectors.
- **FAISS specifically**:
  - Uses L2 distance (Euclidean distance) for similarity
  - IndexFlatL2: Simple but effective for our use case
  - Stores vectors and performs fast nearest neighbor search

## 🗄️ **Data & Database**

### **8. SQLAlchemy**
- **What it is**: Python SQL toolkit and Object-Relational Mapping (ORM) library.
- **Why used**:
  - Abstracts database operations
  - Works with multiple database types
  - Provides Pythonic way to interact with databases
- **In our project**:
  - Defines User, Order, Ticket models
  - Handles SQLite database operations
  - Seeds sample data on startup

### **9. SQLite**
- **What it is**: A lightweight, file-based relational database.
- **Why used**:
  - No separate database server needed
  - Perfect for development and small applications
  - Stores data in a single file (`ecommerce.db`)

## 🌐 **Web Technologies**

### **10. Uvicorn**
- **What it is**: An ASGI web server implementation for Python.
- **Why used**:
  - High-performance ASGI server
  - Built-in support for HTTP/2 and WebSockets
  - Default server for FastAPI applications

### **11. CORS (Cross-Origin Resource Sharing)**
- **What it is**: A security feature that allows web pages to make requests to different domains.
- **In our project**:
  - Allows the HTML interface to communicate with the API
  - Set to allow all origins (`*`) for development

### **12. Pydantic**
- **What it is**: Data validation and settings management using Python type annotations.
- **Why used**:
  - Automatic data validation
  - Type conversion
  - Clear error messages
- **In our project**: Defines `ChatMessage` and `ChatResponse` models

## 📁 **File Formats & Storage**

### **13. Pickle (.pkl files)**
- **What it is**: Python's way of serializing and deserializing objects.
- **Why used**:
  - Stores Python objects (like lists of documents) to disk
  - Fast loading/saving
  - Preserves Python data structures

### **14. JSON**
- **What it is**: JavaScript Object Notation - a lightweight data interchange format.
- **Why used**:
  - API communication between frontend and backend
  - Human-readable data format
  - Universally supported

## 🛠️ **Development Tools**

### **15. Git**
- **What it is**: Distributed version control system.
- **Why used**:
  - Track changes in code
  - Collaborate with others
  - Backup and versioning
- **Commands used**:
  - `git init`: Initialize repository
  - `git add .`: Stage all changes
  - `git commit`: Save changes with message

### **16. Virtual Environment (venv)**
- **What it is**: Isolated Python environment for project dependencies.
- **Why used**:
  - Avoid dependency conflicts
  - Keep project dependencies separate
  - Easy to reproduce environment

### **17. Requirements.txt**
- **What it is**: File listing all Python dependencies with versions.
- **Why used**:
  - Reproduce exact environment
  - Easy installation with `pip install -r requirements.txt`
  - Version pinning prevents compatibility issues

## 🔧 **Project-Specific Concepts**

### **18. Knowledge Base**
- **What it is**: Collection of documents (FAQs) used for RAG retrieval.
- **Structure**:
  - `knowledge_base/` directory
  - `faqs.txt` with Q&A pairs
  - Can be extended with more `.txt` files

### **19. Smart Escalation**
- **What it is**: Automatic detection of when to escalate to human support.
- **How it works**:
  - Checks if response contains escalation keywords
  - Sets `needs_escalation` flag in API response
  - Helps identify complex queries

### **20. Lifespan Events**
- **What it is**: FastAPI's way to run code on startup and shutdown.
- **In our project**:
  - Seeds database on startup
  - Prints status messages
  - Ensures chatbot is ready before accepting requests

## 📊 **Architecture Flow**

```
User Input (Web Interface)
    ↓
FastAPI Endpoint (/chat)
    ↓
ChatBot.process_message()
    ↓
    ├─→ Regex Pattern Matching (Order Numbers)
    │   ├─→ Found? → Query SQLite Database
    │   └─→ Not Found → Continue
    ↓
    ├─→ RAG Pipeline
    │   ├─→ Sentence Transformer → Embedding
    │   ├─→ FAISS Search → Relevant Documents
    │   ├─→ Context + Query → Ollama LLM
    │   └─→ Generate Response
    ↓
    └─→ Fallback: Direct LLM Query
        └─→ Check for Escalation Keywords
```

This combination of technologies creates a robust, local, and cost-effective chatbot solution that can handle both structured queries (like order tracking) and unstructured questions (like general FAQs) while maintaining user privacy and providing accurate responses.
