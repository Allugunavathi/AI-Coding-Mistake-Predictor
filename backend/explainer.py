def explain_code(code):

    explanations = []

    lines = code.split("\n")

    for line in lines:

        line = line.strip()

        if line.startswith("print"):
            explanations.append("🖨️ Prints output to the screen.")

        elif line.startswith("for"):
            explanations.append("🔁 Starts a for loop.")

        elif line.startswith("while"):
            explanations.append("🔄 Starts a while loop.")

        elif line.startswith("if"):
            explanations.append("🤔 Checks a condition.")

        elif line.startswith("elif"):
            explanations.append("➡️ Checks another condition.")

        elif line.startswith("else"):
            explanations.append("📌 Executes when previous conditions are False.")

        elif line.startswith("def"):
            explanations.append("⚙️ Defines a function.")

        elif line.startswith("return"):
            explanations.append("↩️ Returns a value from the function.")

        elif "=" in line:
            explanations.append("📦 Stores a value in a variable.")

        elif line == "":
            continue

        else:
            explanations.append("📄 General Python statement.")

    return explanations