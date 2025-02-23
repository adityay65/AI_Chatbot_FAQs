from sentence_transformers import SentenceTransformer
import numpy as np
import sqlite3

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_faq_embeddings():
    conn = sqlite3.connect('database/faq_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, answer FROM faqs')
    faqs = cursor.fetchall()
    
    questions = [f"{q} {a}" for _, q, a in faqs]
    embeddings = model.encode(questions)
    
    return faqs, embeddings

faqs, faq_embeddings = get_faq_embeddings()

def get_best_faq(query):
    query_embed = model.encode([query])
    similarities = np.dot(faq_embeddings, query_embed.T).flatten()
    max_idx = np.argmax(similarities)
    
    return {
        'question': faqs[max_idx][1],
        'answer': faqs[max_idx][2],
        'confidence': float(similarities[max_idx])
    }
