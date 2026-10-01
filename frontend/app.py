import streamlit as st
import requests

st.set_page_config(
    page_title="AI Coding Mistake Predictor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Coding Mistake Predictor")
st.write("Analyze your Python code using AI & Machine Learning")

# ==========================
# Input Section
# ==========================

uploaded_file = st.file_uploader(
    "📁 Upload a Python File",
    type=["py"]
)

if uploaded_file is not None:

    code = uploaded_file.read().decode("utf-8")

    st.success("✅ Python file uploaded successfully!")

    st.code(code, language="python")

else:

    code = st.text_area(
        "✍️ Enter Python Code",
        height=300,
        placeholder="Write your Python code here..."
    )

# ==========================
# Analyze Button
# ==========================

if st.button("🚀 Analyze Code"):

    if code.strip() == "":

        st.warning("⚠ Please enter Python code.")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"code": code}
            )

            result = response.json()
            # ==========================
            # Status
            # ==========================

            if result["status"] == "Correct":
                st.success(result["message"])
            else:
                st.error(result["message"])

            # ==========================
            # AI Prediction
            # ==========================

            st.subheader("🤖 AI Prediction")
            st.write(result["prediction"])

            # ==========================
            # Explanation
            # ==========================

            st.subheader("📖 Explanation")
            st.info(result["explanation"])

            # ==========================
            # Code Analysis
            # ==========================

            st.subheader("📊 Code Analysis")

            analysis = result["analysis"]

            st.write(f"📄 Total Lines : {analysis['lines']}")
            st.write(f"📦 Variables : {analysis['variables']}")
            st.write(f"⚙️ Functions : {analysis['functions']}")
            st.write(f"🔁 Loops : {analysis['loops']}")
            st.write(f"🤔 If Statements : {analysis['ifs']}")
            st.write(f"🖨️ Print Statements : {analysis['prints']}")
            st.write(f"📥 Imports : {analysis['imports']}")

            # ==========================
            # Suggested Code
            # ==========================

            st.subheader("✅ Suggested Correct Code")
            st.code(result["fixed_code"], language="python")

            # ==========================
            # Code Quality
            # ==========================

            st.subheader("⭐ Code Quality Score")

            score = result["score"]

            st.progress(score / 100)

            st.metric(
                label="Overall Score",
                value=f"{score}/100"
            )

            st.success(f"Readability : {result['readability']}")

            # ==========================
            # Suggestions
            # ==========================

            st.subheader("💡 Suggestions")

            for tip in result["tips"]:
                st.write("•", tip)
                            # ==========================
            # Download Report
            # ==========================

            report = f"""
            ========== AI Coding Report ==========

            Status:
            {result["status"]}

            Prediction:
            {result["prediction"]}

            Score:
            {result["score"]}/100

            Readability:
            {result["readability"]}

            Explanation:
            {result["explanation"]}

            Original Code:
            {code}

            Suggested Code:
            {result["fixed_code"]}
            """

            report += "\nSuggestions:\n"

            for tip in result["tips"]:
                report += f"- {tip}\n"

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="AI_Code_Report.txt",
                mime="text/plain"
            )

        except requests.exceptions.ConnectionError:

            st.error("❌ Cannot connect to FastAPI Backend.")

            st.info("Start the backend using:")

            st.code("uvicorn main:app --reload")

        except Exception as e:

            st.error("❌ Unexpected Error")

            st.exception(e)