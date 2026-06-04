import streamlit as st
import requests
import os
from dotenv import load_dotenv

# =====================================
# LOAD ENVIRONMENT VARIABLES
# =====================================

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    st.error("HF_API_KEY not found in .env file")
    st.stop()

# =====================================
# API CONFIG
# =====================================

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="AI Debugger Pro",
    page_icon="🐞",
    layout="wide"
)

st.title("🐞 AI Debugger Pro")
st.write("Debug, review, and optimize your code using AI.")

# =====================================
# INPUTS
# =====================================

language = st.selectbox(
    "Programming Language",
    [
        "Python",
        "JavaScript",
        "Java",
        "C++",
        "C",
        "Go",
        "Rust"
    ]
)

code = st.text_area(
    "Paste your code here",
    height=350
)

# =====================================
# BUTTONS
# =====================================

col1, col2, col3 = st.columns(3)

debug_clicked = col1.button("🐞 Debug Code")
review_clicked = col2.button("🔍 Review Code")
optimize_clicked = col3.button("⚡ Optimize Code")

# =====================================
# PROCESS REQUEST
# =====================================

if debug_clicked or review_clicked or optimize_clicked:

    if not code.strip():
        st.warning("Please paste some code.")
        st.stop()

    if debug_clicked:

        prompt = f"""
You are an expert software engineer.

Analyze this {language} code.

Return:

# Errors Found

# Fixed Code

# Explanation

# Suggestions

Code:

{code}
"""

    elif review_clicked:

        prompt = f"""
You are a senior software engineer.

Review this {language} code.

Return:

# Code Quality Score (/10)

# Strengths

# Weaknesses

# Best Practice Violations

# Suggested Improvements

Code:

{code}
"""

    else:

        prompt = f"""
You are a performance optimization expert.

Analyze this {language} code.

Return:

# Performance Issues

# Optimized Code

# Time Complexity

# Space Complexity

# Optimization Suggestions

Code:

{code}
"""

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1500
    }

    with st.spinner("Analyzing code..."):

        try:

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:

                result = response.json()

                output = result["choices"][0]["message"]["content"]

                st.success("Analysis Complete!")
                st.markdown(output)

            else:

                st.error(
                    f"API Error {response.status_code}\n\n{response.text}"
                )

        except Exception as e:

            st.error(f"Error: {str(e)}")

# =====================================
# FOOTER
# =====================================

st.divider()

st.caption("AI Debugger Pro • Debug • Review • Optimize")