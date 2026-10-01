from fastapi import FastAPI
from pydantic import BaseModel
import traceback
import joblib
from datetime import datetime
from database import create_database, save_history, get_history

app = FastAPI()

create_database()

# ==========================
# Load AI Model
# ==========================

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# ==========================
# Input Schema
# ==========================

class CodeInput(BaseModel):
    code: str


# ==========================
# Home API
# ==========================

@app.get("/")
def home():
    return {
        "message": "AI Coding Mistake Predictor API is Running!"
    }


# ==========================
# Auto Code Fix
# ==========================

def fix_code(code):

    fixes = {
        "Print(": "print(",
        "Print (": "print(",
        "pritn(": "print(",
        "leng(": "len(",
        "intt(": "int(",
        "flot(": "float(",
        "whille": "while",
        "iff ": "if ",
        "Else": "else",
        "Elif": "elif"
    }

    fixed = code

    for wrong, correct in fixes.items():
        fixed = fixed.replace(wrong, correct)

    return fixed


# ==========================
# Code Quality Score
# ==========================

def calculate_score(code):

    score = 100

    # Empty code
    if len(code.strip()) == 0:
        return 0

    # Small code
    if len(code) < 10:
        score -= 20

    # Runtime mistakes
    if "Print(" in code:
        score -= 20

    if "pritn(" in code:
        score -= 20

    if "leng(" in code:
        score -= 15

    if "intt(" in code:
        score -= 15

    if "flot(" in code:
        score -= 15

    if "whille" in code:
        score -= 20

    if "iff " in code:
        score -= 20

    if "except:" in code:
        score -= 10

    if "\t" in code:
        score -= 5

    if score < 0:
        score = 0

    return score
# ==========================
# Readability
# ==========================

def readability(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Poor"


# ==========================
# Suggestions
# ==========================

def improvement(code):

    tips = []

    if "Print(" in code:
        tips.append("Use print() with a lowercase 'p'.")

    if "pritn(" in code:
        tips.append("Did you mean print()?")

    if "leng(" in code:
        tips.append("Use len() instead of leng().")

    if "intt(" in code:
        tips.append("Use int() instead of intt().")

    if "flot(" in code:
        tips.append("Use float() instead of flot().")

    if "whille" in code:
        tips.append("Use while instead of whille.")

    if "iff " in code:
        tips.append("Use if instead of iff.")

    if "except:" in code:
        tips.append("Catch specific exceptions instead of using a bare except.")

    if len(code.strip()) < 10:
        tips.append("Write more meaningful code.")

    if len(tips) == 0:
        tips.append("Your code follows good coding practices.")

    return tips


# ==========================
# Friendly Error Explanation
# ==========================

def explain_error(error):

    error = str(error)

    if "name" in error.lower() and "not defined" in error.lower():
        return "A variable or function is being used before it is defined."

    elif "syntax" in error.lower():
        return "Python syntax is incorrect. Check brackets, quotes, colons, and indentation."

    elif "division by zero" in error.lower():
        return "A number cannot be divided by zero."

    elif "indent" in error.lower():
        return "Check the indentation. Python uses indentation to define blocks."

    elif "type" in error.lower():
        return "Two incompatible data types are being used together."

    else:
        return error


# ==========================
# Code Analysis
# ==========================

def analyze_code_info(code):

    lines = len(code.splitlines())

    loops = code.count("for ") + code.count("while ")

    functions = code.count("def ")

    ifs = code.count("if ")

    prints = code.count("print(")

    imports = code.count("import ")

    variables = 0

    for line in code.splitlines():

        if "=" in line and "==" not in line and "!=" not in line:
            variables += 1

    analysis = {
        "lines": lines,
        "variables": variables,
        "functions": functions,
        "loops": loops,
        "ifs": ifs,
        "prints": prints,
        "imports": imports
    }

    return analysis
# ==========================
# Analyze API
# ==========================

@app.post("/analyze")
def analyze_code(data: CodeInput):

    code = data.code

    fixed_code = fix_code(code)

    score = calculate_score(code)

    read = readability(score)

    tips = improvement(code)

    analysis = analyze_code_info(code)

    try:

        exec(code)

        features = vectorizer.transform([code])

        prediction = model.predict(features)[0]

        explanation = "Your code executed successfully."

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        save_history(
            code,
            str(prediction),
            score,
            current_time
        )

        return {
            "status": "Correct",
            "message": "No runtime errors found.",
            "prediction": str(prediction),
            "fixed_code": fixed_code,
            "score": score,
            "readability": read,
            "tips": tips,
            "analysis": analysis,
            "explanation": explanation
        }

    except Exception as e:

        features = vectorizer.transform([code])

        prediction = model.predict(features)[0]

        explanation = explain_error(e)

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        save_history(
            code,
            str(prediction),
            score,
            current_time
        )

        return {
            "status": "Error",
            "message": str(e),
            "prediction": str(prediction),
            "fixed_code": fixed_code,
            "score": score,
            "readability": read,
            "tips": tips,
            "analysis": analysis,
            "explanation": explanation
        }
# ==========================
# History API
# ==========================

@app.get("/history")
def history():

    rows = get_history()

    history = []

    for row in rows:

        history.append({

            "id": row[0],
            "code": row[1],
            "prediction": row[2],
            "score": row[3],
            "datetime": row[4]

        })

    return history


# ==========================
# Health Check API
# ==========================

@app.get("/health")
def health():

    return {
        "status": "Running",
        "message": "AI Coding Mistake Predictor Backend is Working!"
    }