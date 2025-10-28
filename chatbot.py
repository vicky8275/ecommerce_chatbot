import requests
from database import SessionLocal, User, Order, Ticket
from rag_engine import RAGEngine
from datetime import datetime
import json
import re

class ChatBot:
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3:latest"  # Using your existing llama3 model
    
    def _call_ollama(self, prompt):
        """Call local Ollama instance"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60  # Increased timeout to 60 seconds
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "I'm having trouble connecting to my AI service. Please try again."
        except Exception as e:
            print(f"Ollama error: {e}")
            return "I'm experiencing technical difficulties. Please try again or contact support."
    
    def _extract_order_number(self, text):
        """Extract order number from text"""
        match = re.search(r'\b\d{5}\b', text)
        return int(match.group()) if match else None
    
    def _query_database(self, query, context=None):
        """Query the database for relevant information"""
        db = SessionLocal()
        try:
            query_lower = query.lower()
            
            # Check for order status queries
            if any(word in query_lower for word in ['order', 'track', 'where is', 'status']):
                order_num = self._extract_order_number(query)
                if order_num:
                    order = db.query(Order).filter(Order.order_id == order_num).first()
                    if order:
                        user = db.query(User).filter(User.user_id == order.user_id).first()
                        return {
                            'type': 'order_found',
                            'order_id': order.order_id,
                            'status': order.status,
                            'items': order.items,
                            'user_name': user.name if user else 'Customer'
                        }
                return {'type': 'order_number_needed'}
            
            return None
        finally:
            db.close()
    
    def _create_ticket(self, user_id, issue_description):
        """Create a support ticket"""
        db = SessionLocal()
        try:
            ticket = Ticket(
                user_id=user_id or 0,
                issue_description=issue_description,
                status='open'
            )
            db.add(ticket)
            db.commit()
            return ticket.ticket_id
        finally:
            db.close()
    
    def process_message(self, user_message, context=None):
        """Main chatbot processing logic"""
        # Step 1: Try database retrieval
        db_result = self._query_database(user_message, context)
        
        if db_result:
            if db_result['type'] == 'order_found':
                return {
                    'response': f"I found your order #{db_result['order_id']}! It's currently {db_result['status']}. Items: {db_result['items']}.",
                    'needs_escalation': False
                }
            elif db_result['type'] == 'order_number_needed':
                return {
                    'response': "I can help you track your order! Could you please provide your order number? It's a 5-digit number you received in your confirmation email.",
                    'needs_escalation': False
                }
        
        # Step 2: Try RAG retrieval
        relevant_docs = self.rag_engine.retrieve(user_message)
        
        if relevant_docs:
            context_info = "\n".join(relevant_docs)
            prompt = f"""You are a helpful customer support chatbot for an e-commerce platform.

Context from knowledge base:
{context_info}

Customer question: {user_message}

Provide a helpful, concise response based on the context. If the context doesn't fully answer the question, say so and offer to escalate to human support."""
            
            response = self._call_ollama(prompt)
            
            # Check if escalation is needed
            needs_escalation = any(word in response.lower() for word in ['escalate', 'human support', 'contact support'])
            
            return {
                'response': response,
                'needs_escalation': needs_escalation
            }
        
        # Step 3: Use generative AI without context
        prompt = f"""You are a helpful customer support chatbot for an e-commerce platform.

Customer question: {user_message}

Provide a helpful response. If you cannot answer confidently, offer to escalate to human support."""
        
        response = self._call_ollama(prompt)
        
        return {
            'response': response,
            'needs_escalation': True
        }