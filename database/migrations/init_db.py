import sqlite3
import json
from pathlib import Path

def init_db():
    conn = sqlite3.connect('database/faq_database.db')
    cursor = conn.cursor()
    
    try:
        # Create table without explicit ID (use autoincrement)
        cursor.execute('''CREATE TABLE IF NOT EXISTS faqs
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         question TEXT NOT NULL,
                         answer TEXT NOT NULL)''')
        
        # Load data from nested structure
        json_path = Path(__file__).parent.parent.parent / 'nlp/data/faq_data_large.json'
        
        with open(json_path, 'r') as f:
            data = json.load(f)
            faqs = data.get('faqs', [])
            
            # Validate structure
            if not isinstance(faqs, list):
                raise ValueError("'faqs' should be an array")
                
            for idx, faq in enumerate(faqs):
                if 'question' not in faq or 'answer' not in faq:
                    raise ValueError(f"FAQ {idx} missing question/answer")
                
                # Insert without explicit ID (let DB handle autoincrement)
                cursor.execute('''
                    INSERT INTO faqs (question, answer)
                    VALUES (?, ?)
                ''', (faq['question'], faq['answer']))
        
        conn.commit()
        print(f"Successfully loaded {len(faqs)} FAQs")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
