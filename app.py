import streamlit as st

st.set_page_config(page_title="SmartQuizzer", layout="centered")

# 🎨 CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}
h1, h2, h3 {
    text-align: center;
}
.card {
    padding: 25px;
    border-radius: 15px;
    background-color: #1e293b;
    margin-top: 20px;
}
.stButton>button {
    border-radius: 10px;
    height: 45px;
    width: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# Redirect if logged in
if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")

# 🧠 HEADER
st.markdown("<h1>🧠 Smart Quizzer AI</h1>", unsafe_allow_html=True)
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)

# 📦 CARD START
st.markdown('<div class="card">', unsafe_allow_html=True)

# ---------------- SIGNUP UI ----------------
if st.session_state.show_signup:

    st.subheader("📝 Create Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email ID")
    new_password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):
            if full_name and email and new_password:
                st.success("Account created successfully 🎉")
                st.session_state.show_signup = False
            else:
                st.error("Please fill all fields")

    with col2:
        if st.button("⬅ Back to Login"):
            st.session_state.show_signup = False

# ---------------- LOGIN UI ----------------
else:

    st.subheader("🔐 Login to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Enter credentials")

    with col2:
        if st.button("Create Account"):
            st.session_state.show_signup = True

    st.markdown("---")

    if st.button("Forgot Password"):
        st.info("Password reset link sent to email")

# 📦 CARD END
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<hr>
<p style='text-align:center;'>Made with ❤️ by SmartQuizzer</p>
""", unsafe_allow_html=True)