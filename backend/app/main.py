# backend/app/main.py

# --- Add these path adjustments FIRST ---
import sys
import os
from pathlib import Path

# Calculate backend directory path (two levels up from this file)
current_file = Path(__file__).resolve()
backend_dir = current_file.parent.parent  # Gets 'backend' directory
sys.path.insert(0, str(backend_dir))

# Now import modules AFTER path adjustment
from nlp.similarity import get_best_faq
from nlp.bias_detection import detect_and_correct_bias

# --- Rest of the Flask application ---
from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    result = get_best_faq(data['query'])
    
    if result['confidence'] < 0.5:
        return jsonify({
            'answer': "I'm not sure about this, let me verify with our team.",
            'confidence': result['confidence']
        })
    
    corrected = detect_and_correct_bias(result['answer'])
    return jsonify({
        'answer': corrected,
        'confidence': result['confidence'],
        'original_answer': result['answer']
    })

@app.route('/faqs', methods=['GET', 'POST'])
def manage_faqs():
    conn = sqlite3.connect('../database/faq_database.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT id, question, answer FROM faqs')
        faqs = [{'id': row[0], 'question': row[1], 'answer': row[2]} 
               for row in cursor.fetchall()]
        return jsonify(faqs)
    
    elif request.method == 'POST':
        data = request.get_json()
        cursor.execute('INSERT INTO faqs (question, answer) VALUES (?, ?)',
                      (data['question'], data['answer']))
        conn.commit()
        return jsonify({'status': 'success', 'id': cursor.lastrowid})

@app.route('/faqs/<int:id>', methods=['PUT', 'DELETE'])
def manage_single_faq(id):
    conn = sqlite3.connect('../database/faq_database.db')
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.get_json()
        cursor.execute('UPDATE faqs SET question=?, answer=? WHERE id=?',
                      (data['question'], data['answer'], id))
        conn.commit()
        return jsonify({'status': 'updated'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM faqs WHERE id=?', (id,))
        conn.commit()
        return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
