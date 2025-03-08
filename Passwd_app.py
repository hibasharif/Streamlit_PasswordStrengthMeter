import streamlit as st
import re
import random
import string
import time

# Custom CSS for dark theme with enhanced styling
dark_theme = """
<style>
    body {
        background-color: #121212;
        color: #ffff;
    }
    .stTextInput input {
        background-color: #eee;
        color: black;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #555;
    }
    .strength-meter {
        height: 12px;
        border-radius: 6px;
        margin-top: 5px;
    }
    .suggestion-box, .history-box {
        background-color: #222;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.15);
    }
    .done-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        text-align: center;
    }
    .done-button:hover {
        background-color: #45a049;
    }
</style>
"""

st.markdown(dark_theme, unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)
st.title("🔒 Password Strength Meter")
st.markdown("Enter a password to check its strength.")

password = st.text_input("Enter Password", type="password")
password_history = st.session_state.get("password_history", [])

def check_strength(password):
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[@$!%*?&]", password))
    
    score = sum([length >= 8, has_upper, has_lower, has_digit, has_special])
    return score

def generate_password():
    characters = string.ascii_letters + string.digits + "@$!%*?&"
    return ''.join(random.choice(characters) for _ in range(12))

def check_common_passwords(password):
    common_passwords = ["123456", "password", "123456789", "qwerty", "abc123"]
    return password in common_passwords

if password:
    # Analyze password strength
    score = check_strength(password)
    
    # Define color coding
    strength_colors = ["#ff4d4d", "#ff944d", "#ffd700", "#9acd32", "#32cd32"]
    
    st.markdown(
        f'<div class="strength-meter" style="background-color: {strength_colors[score]}; width: {((score+1)/5)*100}%"></div>',
        unsafe_allow_html=True
    )
    
    st.subheader("Strength Rating: ")
    st.write(["Very Weak", "Weak", "Medium", "Strong", "Very Strong"][score])
    
    if check_common_passwords(password):
        st.warning("⚠️ This password is commonly used and insecure!")
    
    if score < 4:
        st.markdown("<div class='suggestion-box'><b>Suggestions:</b><br> - Use at least 8 characters<br> - Include uppercase and lowercase letters<br> - Add numbers and special characters</div>", unsafe_allow_html=True)
    
    # Store password history
    password_history.append((password, time.strftime("%Y-%m-%d %H:%M:%S")))
    st.session_state["password_history"] = password_history[-5:]  # Keep last 5 entries
    
    st.subheader("🔑 Generate a Strong Password")
    if st.button("Generate Password"):
        st.text_input("Generated Password", generate_password(), disabled=True)
    
    # Show password history
    if password_history:
        st.subheader("📜 Password Check History")
        st.markdown("<div class='history-box'>", unsafe_allow_html=True)
        for pw, timestamp in reversed(password_history):
            st.write(f"🔹 {pw} (Checked at: {timestamp})")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Password visibility toggle
    show_password = st.checkbox("Show Password")
    if show_password:
        st.text_input("Your Password:", password, disabled=True)
    
    # Done button
    if st.button("Done", key="done-button"):
        st.success("✅ Password check completed!")

st.markdown('</div>', unsafe_allow_html=True)
