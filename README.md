# 📚 AI Study Buddy

An interactive AI-powered study assistant built with Streamlit and Google Gemini. It converts your study notes (via raw text or uploaded PDF) into a revision pack complete with bullet-point summaries, practice multiple-choice questions (MCQs), and key terminology definitions.

## Features

- **Notes Summarization**: Generates concise, bullet-pointed summaries of your study material.
- **Practice MCQs**: Generates 5 multiple-choice questions with answers and explanations.
- **Key Terms**: Extracts critical terms and concepts with simple explanations.
- **Dual Input**: Support for pasted text notes and PDF uploads.

## Prerequisites

- Python 3.10+
- Google Gemini API key ([Get one here](https://aistudio.google.com/))

## Installation & Setup

1. Clone this repository:
   ```bash
   git clone <REPO_URL>
   cd "STUDY BUDY"
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   Copy `.env.example` to `.env` and insert your Gemini API key:
   ```env
   GEMINI_API_KEY="your-api-key-here"
   GEMINI_MODEL="gemini-2.5-flash"
   ```

## Running the App

Run the Streamlit application:
```bash
streamlit run app.py
```