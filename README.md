# AI-Text-Morph

## Introduction
**AI-Text-Morph** is an advanced text summarization and paraphrasing web application built with Streamlit. It allows users to efficiently summarize long texts, generate paraphrased versions, and get readability scores, all in a user-friendly interface. The project combines NLP techniques with a clean front-end experience, making text processing easy and accessible.

---

## Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Python  
- **Database:** SQLite  
- **Libraries & Tools:** `nltk`, `spacy`, `textstat`, `pandas`, `base64`  
- **Version Control:** Git & GitHub  

---

## Project Structure
AI-Text-Morph/
│
├── frontend/ # UI using Streamlit
│ ├── Home.py
│ ├── pages/
│ │ ├── create_account.py
│ │ ├── dashboard.py
│ │ └── profile.py
│ └── assets/
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
├── .gitignore # Files/folders to ignore in Git
└── README.md # Project documentation

---

## Features
- **Home Page:** Landing page with overview and navigation.  
- **Create Account:** Sign up and store credentials securely.  
- **Dashboard:** Main interface for summarization and paraphrasing tasks.  
- **Profile Page:** View account information and settings.  
- **Text Summarization:** Summarize long articles or paragraphs into concise text.  
- **Paraphrasing:** Generate alternative versions of text while retaining meaning.  
- **Readability Scores:** Get readability metrics for input texts to assess clarity.  

---

## Prerequisites
- Python 3.8+ installed  
- Git installed  
- Virtual environment tool (`venv`)  

---

## Installation & Setup
