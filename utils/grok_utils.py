import streamlit as st
import json
from groq import Groq
from PyPDF2 import PdfReader


# -------- PDF TEXT --------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t
    return text[:4000]


# -------- GROQ (WORKING) --------
def generate_questions(text, mcq_count, fill_count):

    from groq import Groq
    import streamlit as st
    import json

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
    Generate a quiz from the text.

    Create:
    - {mcq_count} MCQ questions (each with 4 options)
    - {fill_count} fill in the blanks

    STRICT:
    - Return ONLY JSON
    - No extra text

    Format:
    {{
      "mcq":[
        {{
          "q":"question",
          "options":["A","B","C","D"],
          "answer":"Correct option text"
        }}
      ],
      "fill":[
        {{
          "q":"question",
          "answer":"correct answer"
        }}
      ]
    }}

    TEXT:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content

        start = raw.find("{")
        end = raw.rfind("}") + 1

        data = json.loads(raw[start:end])

        return data

    except Exception as e:
        st.error(f"Error: {e}")
        return {}