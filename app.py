

import streamlit as st
import PyPDF2
import requests

# 🔑 👉 PASTE YOUR OPENROUTER API KEY HERE
API_KEY = "sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 🎯 Title
st.title("🚀 Smart AI Resume Analyzer Pro")
st.markdown("Upload resume → Analyze → ATS Score → Improve Resume")

# 📤 Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# 📄 Job Description
job_desc = st.text_area("Paste Job Description (optional)")

# 🔍 Extract text from PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# 🤖 AI API Call
def call_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return f"Error: {response.text}"

# 🔍 Resume Analysis
def analyze_resume(resume, job_desc):
    prompt = f"""
    Analyze this resume:

    {resume}

    Job Description:
    {job_desc}

    Provide:
    - Resume Score out of 10
    - Strengths
    - Weaknesses
    - Suggestions
    """
    return call_ai(prompt)

# 📊 ATS Score
def ats_score(resume, job_desc):
    if not job_desc:
        return "⚠️ Please provide Job Description."

    prompt = f"""
    Compare resume and job description.

    Resume:
    {resume}

    Job Description:
    {job_desc}

    Provide:
    - ATS Score (%)
    - Matching Skills
    - Missing Skills
    """
    return call_ai(prompt)

# 🧠 Skill Gap Analysis
def skill_gap(resume, job_desc):
    if not job_desc:
        return "⚠️ Please provide Job Description."

    prompt = f"""
    Identify skill gap.

    Resume:
    {resume}

    Job Description:
    {job_desc}

    Provide:
    - Missing Skills
    - Recommended Skills
    - Priority (High/Medium/Low)
    """
    return call_ai(prompt)

# ✨ Resume Rewriter
def rewrite_resume(resume):
    prompt = f"""
    Improve this resume professionally.

    Make it:
    - ATS optimized
    - Strong wording
    - Add impact

    Resume:
    {resume}
    """
    return call_ai(prompt)

# ✉ Email Generator
def generate_email(resume):
    prompt = f"""
    Write a short professional job application email.

    Resume:
    {resume}
    """
    return call_ai(prompt)

# 🚀 MAIN APP
if uploaded_file:
    st.success("✅ Resume uploaded!")

    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Extracted Resume")
    st.text_area("Resume Content", resume_text, height=200)

    # 🔍 Analyze
    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text, job_desc)
        st.subheader("📊 Analysis Result")
        st.markdown(result)

    # 📊 ATS
    if st.button("📊 ATS Score"):
        with st.spinner("Checking ATS..."):
            result = ats_score(resume_text, job_desc)
        st.subheader("📊 ATS Result")
        st.markdown(result)

    # 🧠 Skill Gap
    if st.button("🧠 Skill Gap Analysis"):
        with st.spinner("Analyzing skills..."):
            result = skill_gap(resume_text, job_desc)
        st.subheader("🧠 Skill Gap")
        st.markdown(result)

    # ✨ Improve Resume
    if st.button("✨ Improve Resume"):
        with st.spinner("Improving resume..."):
            result = rewrite_resume(resume_text)
        st.subheader("✨ Improved Resume")
        st.markdown(result)

        st.download_button(
            "📥 Download Improved Resume",
            result,
            "improved_resume.txt"
        )

    # ✉ Email
    if st.button("✉ Generate Email"):
        with st.spinner("Generating email..."):
            result = generate_email(resume_text)
        st.subheader("✉ Email")
        st.markdown(result)