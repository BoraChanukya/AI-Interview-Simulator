import streamlit as st
import PyPDF2
import google.generativeai as genai

# =========================
# Gemini API Key from Streamlit Secrets
# =========================
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# =========================
# Page Title
# =========================
st.title("🎯 AI Interview Simulator")

# =========================
# Upload Resume
# =========================
resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if resume:

    st.success("✅ Resume uploaded successfully")

    # =========================
    # Read Resume PDF
    # =========================
    reader = PyPDF2.PdfReader(resume)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # =========================
    # Show Resume Content
    # =========================
    st.subheader("📄 Resume Content")
    st.write(text)

    # =========================
    # Skill Detection
    # =========================
    skills = [
        "Python",
        "R",
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "Machine Learning",
        "Data Analysis",
        "Power BI",
        "NumPy",
        "Pandas",
        "Artificial Intelligence",
        "Data Science"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    st.subheader("🛠 Detected Skills")
    st.write(found_skills)

    # =========================
    # Generate Questions
    # =========================
    if st.button("Generate Interview Questions"):

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Generate 10 technical interview questions
        for a candidate with the following skills:

        {', '.join(found_skills)}

        Give only numbered questions.
        """

        response = model.generate_content(prompt)

        st.session_state.questions = response.text

        st.subheader("🤖 AI Interview Questions")
        st.write(response.text)

    # =========================
    # Show Questions Again
    # =========================
    if "questions" in st.session_state:

        st.subheader("🤖 AI Interview Questions")
        st.write(st.session_state.questions)

        # =========================
        # Answer Evaluation
        # =========================
        st.subheader("✍ Enter Your Answer")

        user_answer = st.text_area(
            "Type your answer here"
        )

        if st.button("Evaluate Answer"):

            model = genai.GenerativeModel("gemini-2.5-flash")

            evaluation_prompt = f"""
            Interview Questions:

            {st.session_state.questions}

            Candidate Answer:

            {user_answer}

            Evaluate the answer.

            Provide:

            1. Score out of 10
            2. Strengths
            3. Weaknesses
            4. Suggestions for Improvement
            """

            evaluation = model.generate_content(
                evaluation_prompt
            )

            st.subheader("📊 AI Feedback")
            st.write(evaluation.text)