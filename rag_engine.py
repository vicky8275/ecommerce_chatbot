import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

class RAGEngine:
    def __init__(self, knowledge_base_path="knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = "faiss_index.pkl"
        self.docs_path = "documents.pkl"
        
        # Load or create index
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            self._load_index()
            print("✓ Loaded existing knowledge base")
        else:
            self._create_index()
            print("✓ Created and loaded new knowledge base")
    
    def _create_index(self):
        """Create FAISS index from documents"""
        if not os.path.exists(self.knowledge_base_path):
            os.makedirs(self.knowledge_base_path)
            self._create_sample_faqs()
        
        # Load all text files from knowledge base
        documents = []
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.knowledge_base_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Split into chunks
                    chunks = content.split('\n\n')
                    for chunk in chunks:
                        if chunk.strip():
                            documents.append(chunk.strip())
        
        if documents:
            # Create embeddings
            embeddings = self.embedding_model.encode(documents, convert_to_numpy=True)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            # Store documents
            self.documents = documents
            
            # Save index and documents
            self._save_index()
        else:
            # Empty index
            dimension = 384  # all-MiniLM-L6-v2 dimension
            self.index = faiss.IndexFlatL2(dimension)
            self.documents = []
    
    def _save_index(self):
        """Save FAISS index and documents to disk"""
        faiss.write_index(self.index, "faiss_index.bin")
        with open(self.docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def _load_index(self):
        """Load FAISS index and documents from disk"""
        self.index = faiss.read_index("faiss_index.bin")
        with open(self.docs_path, 'rb') as f:
            self.documents = pickle.load(f)
    
    def _create_sample_faqs(self):
        """Create sample FAQ file"""
        faq_content = """Q: How do I track my order?
A: You can track your order by providing your order number to our chatbot or visiting the 'Orders' section in your account.

Q: What is your return policy?
A: We offer a 30-day return policy for most items. Items must be unused and in original packaging. To initiate a return, visit our Returns page or contact support.

Q: How long does shipping take?
A: Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. International orders may take 10-15 business days.

Q: Can I change my shipping address?
A: If your order hasn't shipped yet, you can change the address by contacting customer support immediately. Once shipped, address changes are not possible.

Q: What payment methods do you accept?
A: We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and Apple Pay.

Q: How do I cancel my order?
A: Orders can be cancelled within 24 hours of placement. Visit your order history and click 'Cancel Order' or contact support for assistance."""
        
        with open(os.path.join(self.knowledge_base_path, 'faqs.txt'), 'w', encoding='utf-8') as f:
            f.write(faq_content)
    
    def retrieve(self, query, n_results=2):
        """Retrieve relevant documents for a query"""
        if len(self.documents) == 0:
            return []
        
        # Create query embedding
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        
        # Search in FAISS index
        k = min(n_results, len(self.documents))
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return relevant documents
        results = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        return results