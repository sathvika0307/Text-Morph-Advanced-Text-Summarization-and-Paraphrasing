# 📝 AI-Text-Morph  
*A Text Readability, Summarization, and Paraphrasing Application*

---

## 📖 Description

**AI-Text-Morph** is a lightweight NLP-based application that allows users to **analyze, summarize, and paraphrase text** through an intuitive **Streamlit interface.**

Users can securely log in, then either **upload a file** or **paste text** directly into the platform. Once text is provided, the system offers multiple processing options:

- **Readability Analysis** – Evaluate text complexity using readability scores.

- **Summarization** – Generate concise summaries in **small, medium, or long lengths**.

- **Paraphrasing** – Rephrase text with **easy, medium, or advanced complexity**.

All processed outputs are securely stored in a **SQLite database** for consistency and future reference.

This project demonstrates the **practical integration of authentication, database storage, and rule-based NLP algorithms** within an interactive interface, making it both an educational and functional solution for text processing.

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

├── frontend/                          # UI layer built with Streamlit

│   ├── Home.py                        # Landing page of the application

│   ├── pages/                         # Multi-page navigation in Streamlit

│   │   ├── 1_Create_Account.py        # User registration and account creation

│   │   ├── 2_Dashboard.py             # Main dashboard for text processing

│   │   └── 3_Profile.py               # User profile and settings

│   └── assets/                        # Static resources for UI

│       └── Background_Image.jpg       # Background image for styling

│

├── backend/                           # Backend logic & text processing modules

│   ├── utils.py                       # Helper functions (auth, file handling, etc.)

│   ├── fix_db.py                      # Script to fix or reset database issues

│   ├── text_readability.py            # Readability analysis implementation

│   ├── summarization.py               # Summarization logic (small, medium, large)

│   └── paraphrasing.py                # Paraphrasing logic (basic, medium, advanced)

│

├── database/                          # Database files and handlers

│   ├── user_db.py                     # Database operations (insert, fetch, update)

│   └── user.db                        # SQLite database storing user data & text history

│

├── requirements.txt                   # Python dependencies

├── .gitignore                         # Ignored files/folders for version control

└── README.md                          # Project documentation

---

## 🖥 Prerequisites

- *Python 3.10+*

- *pip* for dependency management
   
- *Virtual environment* (recommended)
  
- *SQLite* (already included with Python)

  ---

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
