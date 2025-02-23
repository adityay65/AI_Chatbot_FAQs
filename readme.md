# AI Chatbot for FAQs

An AI-powered chatbot that provides FAQ responses with real-time bias detection and self-correction capabilities. Built with React, Flask, and BERT embeddings.


## Key Features
- **NLP-Powered FAQ Matching** using Sentence Transformers
- **Bias Detection System** with pattern-based correction
- **CRUD Operations** for FAQ management
- **Confidence Thresholding** (answers under 50% confidence are declined)
- **React Frontend** with admin dashboard
- **SQLite Database** with JSON seeding

## Installation 🛠️

### Prerequisites
- Python 3.10+
- Node.js 18.x
- npm

### Backend Setup
git clone https://github.com/adityay65/AI_Chatbot_FAQs
cd AI_Chatbot_FAQs/backend

Install dependencies
pip install -r requirements.txt

Initialize database
python database/migrations/init_db.py

Start server
python app/main.py

### Frontend Setup

cd ../frontend
npm install
npm start

## API Documentation
**Base URL:** `http://localhost:5000`

| Endpoint       | Method | Description                |
|----------------|--------|----------------------------|
| `/query`       | POST   | Submit user query          |
| `/faqs`        | GET    | List all FAQs              |
| `/faqs`        | POST   | Create new FAQ             |
| `/faqs/{id}`   | PUT    | Update existing FAQ        |
| `/faqs/{id}`   | DELETE | Remove FAQ                 |

## Project Structure

AI_Chatbot_FAQs/
├── frontend/ # React app
│ ├── public/
│ └── src/
├── backend/ # Flask API
│ ├── app/
│ ├── nlp/
│ └── database/
├── nlp/
│ └── data/ # FAQ datasets
└── docs/ # Documentation


## Configuration
1. Place `faq_data_large.json` in `/nlp/data`
2. Create `.env` file:

