# 📝 AI-Text-Morph - A Summarization and Paraphrasing Project

---

## 📖 Description
*AI-Text-Morph* is a lightweight NLP-based project that allows users to *summarize* and *paraphrase* text using modern AI models.  
The application provides a simple *Streamlit-based frontend* for interaction, with a *FastAPI backend* handling authentication, text processing, and database operations.  

It’s designed as an educational and practical project that demonstrates *authentication, database integration, NLP model usage, and frontend-backend connectivity*.

---

## ⚙ Tech Stack

- *Core:* Python 3.10/3, FastAPI, Uvicorn, Streamlit
  
- *Authentication:* python-jose, passlib[bcrypt], bcrypt
  
- *Database:* SQLite (lightweight, built into Python)
  
- *AI/NLP:* Hugging Face Transformers, PyTorch, SentencePiece, NLTK
   
- *Translation Support:* googletrans, Hugging Face Transformers
  
- *Utilities:* Pydantic, httpx, python-dotenv  

---

## 🚀 Features

- 🔐 *User Authentication:* Register, login, and secure profile management
   
- 📝 *Text Summarization:* Generate concise summaries from longer passages
   
- 🔄 *Text Paraphrasing:* Reword text while preserving meaning
  
- 🌍 *Optional Translation:* Translate summarized/paraphrased text into multiple languages
  
- 👤 *Profile Management:* Update name, age group, and preferred language
  
- 🖼 *Streamlit Frontend:* Clean and interactive interface with backend health check  

---

## 📂 Project Structure

AI-Text-Morph/

│

├── frontend/ # UI using Streamlit

│ ├── Home.py # Landing page

│ ├── pages/ # Multi-page Streamlit navigation

│ │ ├── create_account.py

│ │ ├── dashboard.py

│ │ └── profile.py

│ └── assets/ # Static resources

│ └── Background_Image.jpg

│

├── backend/ # Backend logic & utility functions

│ ├── utils.py

│ └── fix_db.py

│

├── database/ # Database files

│ ├── user_db.py

│ └── user.db

│

├── requirements.txt # Python dependencies

├── .gitignore # Ignored files/folders

└── README.md # Documentation

---

## 🛠 Prerequisites
- *Python 3.10 or later*
   
- *Pip* (Python package manager)
  
- *Virtual Environment* (recommended)
  
- Internet connection (for model downloads and translation APIs)

  ---

### Installation Steps

## Create virtual environment
python -m venv .venv

source .venv/bin/activate   # Linux/Mac

.\.venv\Scripts\activate    # Windows

## Install dependencies
pip install -r requirements.txt

---

## 📖 Learning Outcomes

By building and using *AI-Text-Morph*, you will:

- Understand how to integrate *FastAPI (backend)* with *Streamlit (frontend)*.
  
- Learn to implement *secure authentication* with password hashing and token-based methods.
    
- Gain experience in *SQLite database management* with Python (SQLAlchemy/Pydantic).
  
- Explore *Natural Language Processing (NLP)* tasks such as summarization, transformation, and translation.
    
- Learn to use *Hugging Face Transformers* and *PyTorch* for AI model integration.
  
- Practice building *modular project structures* for maintainable codebases.
  
- Understand how to manage *environment variables* with python-dotenv for secure configuration.
   
- Develop skills in *UI/UX with Streamlit* for building interactive applications.
    
- Learn how to *containerize or extend* the project for deployment (future enhancement).
