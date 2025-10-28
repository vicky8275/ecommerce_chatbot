# E-Commerce Customer Support Chatbot

A RAG-powered customer support chatbot using Ollama (local LLM), FastAPI, and FAISS for an e-commerce platform.

## 🎯 Features

- **Retrieval-Augmented Generation (RAG)** - Combines vector search with LLM generation
- **Database Integration** - Real-time order tracking from SQLite database
- **Local LLM** - Uses Ollama with llama3:latest (no API costs!)
- **Knowledge Base** - FAQ retrieval using FAISS vector database
- **Smart Escalation** - Automatically detects when to escalate to human support
- **RESTful API** - Easy integration with FastAPI
- **Web Interface** - Modern chat UI served at the root endpoint

## 📋 Prerequisites

- Python 3.8+
- Ollama installed with llama3:latest model (✅ You already have this!)

## 🚀 Installation

### 1. Create Project Directory

```bash
mkdir ecommerce_chatbot
cd ecommerce_chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Project Structure

Create these files in your project directory:

```
ecommerce_chatbot/
├── app.py              # Main FastAPI application
├── chatbot.py          # Core chatbot logic
├── database.py         # Database models and setup
├── rag_engine.py       # RAG implementation
├── index.html          # Web chat interface
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

**Note:** The following will be auto-created when you run the app:
- `knowledge_base/` folder with `faqs.txt`
- `faiss_index.bin` FAISS vector index
- `documents.pkl` Pickled document chunks
- `ecommerce.db` SQLite database

## 🏃 Running the Application

### Step 1: Make Sure Ollama is Running

```bash
# Check if Ollama is running
ollama list

# If not running, start it (usually runs automatically)
ollama serve
```

### Step 2: Start the Chatbot Server

```bash
python app.py
```

You should see:
```
🚀 Starting E-Commerce Chatbot...
✓ Database seeded with sample data
✓ Loaded existing knowledge base
✓ Chatbot ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Access the Web Interface

Open your browser and navigate to: `http://localhost:8000`

The web interface provides a modern chat UI for interacting with the chatbot.

## 📝 API Usage

### Endpoint: `/chat`

**Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Where is my order 12345?"}'
```

**Response:**
```json
{
  "response": "I found your order #12345! It's currently shipped. Items: Running Shoes - Size 10.",
  "needs_escalation": false
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🧪 Sample Test Queries

1. **Order Tracking:**
   - "Where is my order 12345?"
   - "Track order 12346"
   - "What's the status of my order?"

2. **FAQ Questions:**
   - "What's your return policy?"
   - "How long does shipping take?"
   - "What payment methods do you accept?"
   - "Can I cancel my order?"

3. **Escalation Scenarios:**
   - "I need to change my shipping address"
   - "I want to speak to a human"

## 🗄️ Sample Database Data

The database is automatically populated with:

**Users:**
- User 1: John Doe (john@example.com)
- User 2: Jane Smith (jane@example.com)

**Orders:**
- Order 12345: Running Shoes - Status: shipped
- Order 12346: Laptop Bag - Status: delivered
- Order 12347: Wireless Headphones - Status: processing

## 🔧 Configuration

### Change LLM Model

In `chatbot.py`, modify:
```python
self.model = "llama3:latest"  # Change to "phi3:latest" if preferred
```

### Adjust RAG Results

In `chatbot.py`, when calling `retrieve()`:
```python
relevant_docs = self.rag_engine.retrieve(user_message, n_results=3)  # Default is 2
```

### Add More FAQs

Edit `knowledge_base/faqs.txt` (created after first run) or add new `.txt` files to the `knowledge_base/` folder.

## 🛠️ Troubleshooting

### Ollama Connection Error

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# If not working, restart Ollama
# Windows: Restart Ollama app
# Mac/Linux: ollama serve
```

### Database Issues

```bash
# Delete and recreate database
rm ecommerce.db
rm -rf chroma_db/

# Restart the app
python app.py
```

### FAISS Index Errors

```bash
# Delete vector index and documents
rm faiss_index.bin documents.pkl

# Restart app to rebuild
python app.py
```

### Port Already in Use

In `app.py`, change the port:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

## 📊 Architecture

```
User Query (Web/API)
    ↓
FastAPI Endpoint
    ↓
ChatBot.process_message()
    ↓
    ├─→ Database Query (SQLite)
    │   ├─→ Order found? → Return order info
    │   └─→ No match → Continue
    ↓
    ├─→ RAG Retrieval (FAISS)
    │   ├─→ Relevant docs found? → Use with LLM
    │   └─→ No match → Continue
    ↓
    └─→ Generative AI (Ollama)
        └─→ Generate response + check escalation
```

## 🎓 Learning Resources

### Understanding RAG
- RAG = Retrieval-Augmented Generation
- Combines searching relevant documents with AI generation
- More accurate than pure LLM responses

### Key Components
- **FAISS**: Efficient vector similarity search for embeddings
- **Sentence Transformers**: Converts text to vectors
- **Ollama**: Local LLM for generating responses
- **SQLAlchemy**: ORM for database operations
- **FastAPI**: Web framework for API and serving HTML

## 🚀 Next Steps

1. **User Authentication** - Add JWT tokens for user sessions
2. **Conversation Memory** - Store chat history for context
3. **More Intent Detection** - Handle returns, cancellations, etc.
4. **Logging** - Add proper logging for debugging
5. **Streaming Responses** - Make Ollama stream responses in real-time
6. **Multi-language Support** - Add support for multiple languages

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this chatbot for your needs!

---

**Built with ❤️ using Python, FastAPI, Ollama, and FAISS**
