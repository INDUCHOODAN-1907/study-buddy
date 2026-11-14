"""
AI Study Buddy: turns notes into a quick revision pack.
Flow: Input (notes text / PDF) -> Gemini AI model -> Output on screen
"""
import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

# ---------- 1. SETUP ----------
load_dotenv()  # reads the .env file so the API key stays out of the code
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def get_api_key():
    """Look for the key in .env first, then in Streamlit secrets (for hosting)."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


# ---------- 2. HELPER FUNCTIONS ----------
def read_pdf(uploaded_file):
    """Extract text from every page of an uploaded PDF."""
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def build_prompt(notes):
    """The instruction we send to Gemini. Asking for JSON makes the output easy to display."""
    return f"""You are a helpful study assistant for a first-year engineering student.
Using ONLY the notes below, create a revision pack.

Return ONLY valid JSON in exactly this format:
{{
  "summary": ["5 to 6 short bullet points"],
  "mcqs": [
    {{
      "question": "question text",
      "options": ["option 1", "option 2", "option 3", "option 4"],
      "answer": "A, B, C or D",
      "explanation": "one line on why this is correct"
    }}
  ],
  "key_terms": [
    {{"term": "word", "meaning": "simple meaning in one line"}}
  ]
}}

Rules: exactly 5 MCQs, exactly 3 key terms, simple English.

NOTES:
{notes}
"""


def generate_pack(client, notes):
    """Send notes to Gemini and convert its JSON reply into a Python dictionary."""
    response = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(notes),
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)


# ---------- 3. SCREEN (UI) ----------
st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("📚 AI Study Buddy")
st.caption("Paste your notes or upload a PDF and get a quick revision pack.")

api_key = get_api_key()
if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

mode = st.radio("How do you want to give your notes?", ["Paste text", "Upload PDF"], horizontal=True)

notes = ""
if mode == "Paste text":
    notes = st.text_area("Paste your notes here", height=250)
else:
    pdf = st.file_uploader("Upload a PDF", type="pdf")
    if pdf:
        notes = read_pdf(pdf)
        st.success(f"PDF read: {len(notes)} characters found.")

if st.button("Generate Revision Pack", type="primary"):
    if len(notes.strip()) < 50:
        st.warning("Please give some more notes (at least a few lines).")
    else:
        with st.spinner("Gemini is preparing your pack..."):
            try:
                pack = generate_pack(client, notes[:30000])  # limit size for safety
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        # ---------- 4. OUTPUT ----------
        st.header("📝 Summary")
        for point in pack["summary"]:
            st.markdown(f"- {point}")

        st.header("❓ Practice Questions")
        for i, q in enumerate(pack["mcqs"], start=1):
            st.markdown(f"**Q{i}. {q['question']}**")
            for letter, option in zip("ABCD", q["options"]):
                st.markdown(f"{letter}. {option}")
            with st.expander("Show answer"):
                st.markdown(f"**Answer: {q['answer']}**. {q['explanation']}")

        st.header("🔑 Key Terms")
        for t in pack["key_terms"]:
            st.markdown(f"- **{t['term']}**: {t['meaning']}")