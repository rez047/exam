from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "final_mcq_only_cbt"

USERS = {"student": "1234"}

# =========================
# 50 MCQs ONLY (NO CODE INPUTS)
# =========================
QUESTION_BANK = [
    # Flask & Web
    {"q": "What is Flask used for?", "options": ["Web framework", "Database", "Game engine", "OS"], "answer": "Web framework"},
    {"q": "What does __name__ represent?", "options": ["Module name", "File size", "Loop counter", "Variable"], "answer": "Module name"},
    {"q": "Which function renders HTML?", "options": ["render_template", "print", "input", "run"], "answer": "render_template"},
    {"q": "Which HTTP method sends data securely?", "options": ["POST", "GET", "DELETE", "PATCH"], "answer": "POST"},
    {"q": "Flask uses which template engine?", "options": ["Jinja2", "React", "Blade", "Twig"], "answer": "Jinja2"},

    # Python basics
    {"q": "What is a variable?", "options": ["Storage for data", "Loop", "Function", "Class"], "answer": "Storage for data"},
    {"q": "What is a function?", "options": ["Reusable block of code", "File", "OS", "Server"], "answer": "Reusable block of code"},
    {"q": "What is a loop used for?", "options": ["Repetition", "Encryption", "Storage", "Rendering"], "answer": "Repetition"},
    {"q": "What keyword defines a function?", "options": ["def", "func", "define", "function"], "answer": "def"},
    {"q": "What is debugging?", "options": ["Finding errors", "Writing code", "Deleting files", "Installing apps"], "answer": "Finding errors"},

    # Web basics
    {"q": "What is HTML used for?", "options": ["Structure", "Logic", "Database", "AI"], "answer": "Structure"},
    {"q": "What is CSS used for?", "options": ["Styling", "Logic", "Server", "Compiler"], "answer": "Styling"},
    {"q": "What is JavaScript used for?", "options": ["Interactivity", "Database", "OS", "Hardware"], "answer": "Interactivity"},
    {"q": "What is API?", "options": ["Interface", "Database", "OS", "Compiler"], "answer": "Interface"},
    {"q": "What is JSON?", "options": ["Data format", "Language", "OS", "Tool"], "answer": "Data format"},

    # Networking & backend
    {"q": "What does GET do?", "options": ["Fetch data", "Send data", "Delete data", "Encrypt data"], "answer": "Fetch data"},
    {"q": "What is a server?", "options": ["Host system", "User device", "Browser", "File"], "answer": "Host system"},
    {"q": "What is a client?", "options": ["User device", "Server", "Database", "Kernel"], "answer": "User device"},
    {"q": "What is a database?", "options": ["Data storage", "Browser", "OS", "Compiler"], "answer": "Data storage"},
    {"q": "What is SQL?", "options": ["Query language", "OS", "Game engine", "Framework"], "answer": "Query language"},

    # Python advanced basics
    {"q": "What is a list?", "options": ["Collection", "Loop", "Function", "Server"], "answer": "Collection"},
    {"q": "What is a dictionary?", "options": ["Key-value store", "Loop", "Function", "Class"], "answer": "Key-value store"},
    {"q": "What is a tuple?", "options": ["Immutable list", "Loop", "Function", "Server"], "answer": "Immutable list"},
    {"q": "What is a class?", "options": ["Blueprint", "Variable", "Loop", "File"], "answer": "Blueprint"},
    {"q": "What is an object?", "options": ["Instance of class", "Loop", "File", "OS"], "answer": "Instance of class"},

    # Additional 25 mixed MCQs
    {"q": "What is indentation in Python?", "options": ["Code structure", "Error", "Loop", "Database"], "answer": "Code structure"},
    {"q": "What is a bug?", "options": ["Error", "Feature", "App", "System"], "answer": "Error"},
    {"q": "What is syntax error?", "options": ["Rule violation", "Runtime feature", "OS issue", "Network issue"], "answer": "Rule violation"},
    {"q": "What is runtime error?", "options": ["Execution error", "Design feature", "Loop", "Variable"], "answer": "Execution error"},
    {"q": "What is boolean?", "options": ["True/False", "Number", "String", "File"], "answer": "True/False"},

    {"q": "What is a loop type 'for' used for?", "options": ["Iteration", "Condition", "Function", "Class"], "answer": "Iteration"},
    {"q": "What is 'while' loop?", "options": ["Condition loop", "Fixed loop", "Class", "Function"], "answer": "Condition loop"},
    {"q": "What is return used for?", "options": ["Output value", "Input", "Loop", "Variable"], "answer": "Output value"},
    {"q": "What is import used for?", "options": ["Load module", "Delete file", "Run system", "Compile"], "answer": "Load module"},
    {"q": "What is a module?", "options": ["Python file", "Loop", "Server", "Database"], "answer": "Python file"},

    {"q": "What is session in Flask?", "options": ["User tracking", "Database", "Loop", "File"], "answer": "User tracking"},
    {"q": "What is request object?", "options": ["Input handler", "Output handler", "Loop", "System"], "answer": "Input handler"},
    {"q": "What is response?", "options": ["Server output", "Input", "Loop", "File"], "answer": "Server output"},
    {"q": "What is Flask app?", "options": ["Application object", "Database", "Loop", "File"], "answer": "Application object"},
    {"q": "What is routing in Flask?", "options": ["URL mapping", "Database", "Loop", "File"], "answer": "URL mapping"},

    {"q": "What is HTML tag?", "options": ["Element", "Loop", "Function", "Database"], "answer": "Element"},
    {"q": "What is CSS selector?", "options": ["Target element", "Loop", "Function", "OS"], "answer": "Target element"},
    {"q": "What is DOM?", "options": ["Document structure", "Database", "OS", "Compiler"], "answer": "Document structure"},
    {"q": "What is frontend?", "options": ["Client side", "Server side", "Database", "Kernel"], "answer": "Client side"},
    {"q": "What is backend?", "options": ["Server side", "Client side", "Browser", "OS"], "answer": "Server side"}
]

# =========================
# BUILD EXAM
# =========================
def generate_exam():
    exam = QUESTION_BANK.copy()
    random.shuffle(exam)
    session["exam"] = exam


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if USERS.get(request.form.get("username")) == request.form.get("password"):
            session["user"] = "student"
            generate_exam()
            return redirect("/exam")

    return render_template("exam.html", mode="login")


# =========================
# EXAM
# =========================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "user" not in session:
        return redirect("/")

    exam = session.get("exam", [])

    if request.method == "POST":
        score = 0
        results = []

        for i, q in enumerate(exam):
            user = request.form.get(f"q{i}")
            correct = q["answer"]

            mark = 2 if user == correct else 0
            score += mark

            results.append({
                "question": q["q"],
                "user": user,
                "correct": correct,
                "marks": mark
            })

        return render_template("exam.html", mode="result", score=score, results=results)

    return render_template("exam.html", mode="exam", exam=exam)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
