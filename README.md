# 💻 Tech Gadget & Laptop Recommender

An AI-powered laptop recommendation agent that helps students choose a laptop based on their budget, use case, hardware requirements, and AI/ML needs.

## 🚀 Features

- Extracts the user's laptop budget and requirements
- Filters laptops using a budget-checking tool
- Uses FAISS for semantic search
- Uses RAG to retrieve laptop, processor, and review information
- Uses LangGraph to organize the AI agent workflow
- Uses Gemini AI to generate the final recommendation
- Provides an interactive Streamlit web interface

## 🧠 Agent Workflow

User Question
      ↓
Requirement Extraction
      ↓
Budget Checking Tool
      ↓
FAISS Vector Search
      ↓
RAG Knowledge Retrieval
      ↓
Gemini AI Recommendation
      ↓
Final Laptop Recommendation

## 🛠️ Technologies Used

- Python
- Google Gemini API
- LangGraph
- LangChain
- FAISS
- RAG
- Streamlit
- Python-dotenv

## 📂 Project Structure

```text
tech-gadget-recommender/
│
├── data/
│   ├── laptops.txt
│   ├── processors.txt
│   └── reviews.txt
│
├── faiss_index/
│
├── app.py
├── streamlit_app.py
├── budget_tool.py
├── create_vector_store.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md

⚙️ Setup
1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the project
cd tech-gadget-recommender
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment

Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Configure Gemini API Key

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key_here

Never upload your real API key to GitHub.

▶️ Run the AI Agent
python app.py
🌐 Run the Streamlit Application
streamlit run streamlit_app.py
💡 Example

Example user request:

I am a B.Tech AI/ML student. My budget is 80000.
I need a laptop for Python, machine learning,
deep learning and college work.

The agent analyzes the requirements, checks the available laptops within the budget, retrieves relevant information from the knowledge base, and generates a recommendation.

📚 Knowledge Base

The RAG knowledge base contains:

Laptop specifications
Processor information
Laptop review summaries

The documents are converted into embeddings and stored in a FAISS vector database.

🎯 Purpose

This project demonstrates how AI agents can combine:

LLMs
RAG
Vector databases
Tools
LangGraph workflows
Web applications

to create a practical recommendation system.

👨‍💻 Author

Veera Chakradhar

B.Tech Artificial Intelligence & Machine Learning