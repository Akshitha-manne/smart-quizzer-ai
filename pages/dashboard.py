import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import json
import os
from utils.grok_utils import extract_text_from_pdf, generate_questions

st.set_page_config(layout="wide")

# 🎨 CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.stButton>button {
    border-radius: 10px;
    height: 40px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 🌤 Greeting
hour = datetime.datetime.now().hour
greeting = "Good Morning ☀️" if hour < 12 else "Good Afternoon 🌤️" if hour < 18 else "Good Evening 🌙"
st.markdown(f"### {greeting}, ready to learn?")

# HEADER
st.markdown("<h1 style='text-align:center;'>📊 Smart Quizzer Dashboard</h1>", unsafe_allow_html=True)

# 🎮 Banner
st.markdown("""
<div class="card">
<h2>🎮 Smart Quiz Arena</h2>
<p>Compete, Learn, Level Up 🚀</p>
</div>
""", unsafe_allow_html=True)

# 🔐 Logout
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

st.markdown("---")

# NAVIGATION
col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
with col2:
    if st.button("📝 Quiz"):
        st.session_state.page = "Quiz"
with col3:
    if st.button("📊 Results"):
        st.session_state.page = "Results"
with col4:
    if st.button("📈 Analytics"):
        st.session_state.page = "Analytics"
with col5:
    if st.button("🏆 Leaderboard"):
        st.session_state.page = "Leaderboard"

st.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- HOME ----------------
if st.session_state.page == "Home":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Upload PDF to Generate Questions")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF processed!")

    col1, col2 = st.columns(2)

    with col1:
        mcq_count = st.number_input("Number of MCQs", min_value=1, max_value=20, value=5)
    with col2:
        fill_count = st.number_input("Fill in the blanks", min_value=0, max_value=10, value=2)

    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("🚀 Generate Questions"):

        if "pdf_text" not in st.session_state:
            st.warning("Upload PDF first")
        else:
            with st.spinner("🤖 Generating smart questions..."):
                questions = generate_questions(
                    st.session_state.pdf_text,
                    mcq_count,
                    fill_count
                )

            if questions:
                st.session_state.questions = questions
                st.success("Questions Generated!")
            else:
                st.error("Failed to generate questions")

    if st.button("▶ Start Quiz"):
        st.session_state.page = "Quiz"
        st.session_state.start_time = time.time()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- QUIZ ----------------
elif st.session_state.page == "Quiz":

    st.header("📝 Quiz")

    if "start_time" in st.session_state:
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 60 - elapsed)
        st.warning(f"⏳ Time Remaining: {remaining}s")

        if remaining == 0:
            st.session_state.page = "Results"

    if "questions" not in st.session_state:
        st.warning("Generate questions first")
    else:

        user_answers = []
        score = 0

        all_questions = []
        if "mcq" in st.session_state.questions:
            all_questions += st.session_state.questions["mcq"]
        if "fill" in st.session_state.questions:
            all_questions += st.session_state.questions["fill"]

        st.session_state.all_questions = all_questions  # 🔥 FIX

        st.markdown("### 🤖 AI Quiz Assistant")

        for i, q in enumerate(all_questions):

            progress = (i + 1) / len(all_questions)
            st.progress(progress)

            st.markdown(f"""
            <div class="card">
            🤖 <b>Question {i+1}:</b><br>{q['q']}
            </div>
            """, unsafe_allow_html=True)

            if "options" in q:
                ans = st.radio("Your answer", q["options"], key=f"q{i}", index=None)
            else:
                ans = st.text_input("Your answer", key=f"q{i}")

            user_answers.append(ans)

        if st.button("✅ Submit Quiz"):

            for i, q in enumerate(all_questions):
                correct_answer = q["answer"]

                if correct_answer in ["A", "B", "C", "D"]:
                    index_map = {"A": 0, "B": 1, "C": 2, "D": 3}
                    correct_answer = q["options"][index_map[correct_answer]]

                if user_answers[i] is not None and str(user_answers[i]).strip().lower() == str(correct_answer).strip().lower():
                    score += 1

            not_attempted = user_answers.count(None)

            st.session_state.score = score
            st.session_state.total = len(all_questions)
            st.session_state.not_attempted = not_attempted
            st.session_state.page = "Results"

# ---------------- RESULTS ----------------
elif st.session_state.page == "Results":

    st.header("📊 Results")

    if "score" in st.session_state:

        score = st.session_state.score
        total = st.session_state.total

        st.success(f"Score: {score}/{total}")

        accuracy = (score / total) * 100
        st.info(f"Accuracy: {accuracy:.2f}%")

        # 🎮 XP SYSTEM
        if "xp" not in st.session_state:
            st.session_state.xp = 0

        st.session_state.xp += score * 10
        level = st.session_state.xp // 50

        st.markdown(f"### 🎮 Level: {level}")
        st.markdown(f"💎 XP: {st.session_state.xp}")
        st.progress((st.session_state.xp % 50) / 50)

        # 🎉 Feedback + Badges
        if score == total:
            st.balloons()
            st.success("🏆 Quiz Master Badge!")
        elif score > total/2:
            st.success("🥈 Good Performer Badge!")
        else:
            st.info("📘 Beginner Badge")

        # 🧠 AI Explanation
        st.markdown("### 🧠 AI Explanation")

        all_questions = st.session_state.get("all_questions", [])

        for q in all_questions:
            st.markdown(f"""
            <div class="card">
            <b>Q:</b> {q['q']} <br>
            <b>Answer:</b> {q['answer']} <br>
            <b>Explanation:</b> Based on your PDF content.
            </div>
            """, unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
elif st.session_state.page == "Analytics":

    st.header("📈 Analytics")

    if "score" in st.session_state:

        score = st.session_state.score
        total = st.session_state.total
        not_attempted = st.session_state.get("not_attempted", 0)

        wrong = total - score - not_attempted

        st.bar_chart({
            "Correct": score,
            "Wrong": wrong,
            "Not Attempted": not_attempted
        })

# ---------------- LEADERBOARD ----------------
elif st.session_state.page == "Leaderboard":

    st.header("🏆 Leaderboard")

    file = "leaderboard.json"

    if os.path.exists(file):
        with open(file, "r") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []

    score = st.session_state.get("score", 0)

    leaderboard.append({"name": "You", "score": score})

    with open(file, "w") as f:
        json.dump(leaderboard, f)

    df = pd.DataFrame(leaderboard)
    df = df.sort_values(by="score", ascending=False)

    st.dataframe(df, use_container_width=True)