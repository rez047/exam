from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "final_cbt_50_complete"

USERS = {"student": "1234"}

# =========================
# SECTION A: MCQs (25 QUESTIONS)
# =========================
MCQ = [
    {"q": "What is Flask mainly used for?", "options": ["Web development", "Game development", "OS design", "Networking hardware"], "answer": "Web development"},
    {"q": "What does __name__ represent in Flask?", "options": ["Module name", "File size", "Loop counter", "Function name"], "answer": "Module name"},
    {"q": "Which function renders HTML in Flask?", "options": ["render_template", "print", "input", "execute"], "answer": "render_template"},
    {"q": "Which HTTP method is used to send form data?", "options": ["POST", "GET", "DELETE", "HEAD"], "answer": "POST"},
    {"q": "What is Jinja2 in Flask?", "options": ["Template engine", "Database", "Compiler", "OS"], "answer": "Template engine"},

    {"q": "Which keyword defines a function in Python?", "options": ["def", "func", "function", "define"], "answer": "def"},
    {"q": "What is a variable?", "options": ["Storage for data", "Loop type", "Function type", "Server"], "answer": "Storage for data"},
    {"q": "What is a loop used for?", "options": ["Repetition", "Encryption", "Storage", "Compilation"], "answer": "Repetition"},
    {"q": "What is debugging?", "options": ["Finding errors", "Writing code", "Running apps", "Deleting files"], "answer": "Finding errors"},
    {"q": "What is Python?", "options": ["Programming language", "Browser", "Database", "Hardware"], "answer": "Programming language"},

    {"q": "What is HTML used for?", "options": ["Structure of web pages", "Database storage", "AI training", "Networking"], "answer": "Structure of web pages"},
    {"q": "What is CSS used for?", "options": ["Styling web pages", "Logic", "Backend", "Database"], "answer": "Styling web pages"},
    {"q": "What is JavaScript used for?", "options": ["Interactivity", "Server management", "OS design", "Hardware control"], "answer": "Interactivity"},
    {"q": "What is API?", "options": ["Application interface", "Operating system", "Compiler", "Database"], "answer": "Application interface"},
    {"q": "What is JSON?", "options": ["Data format", "Language", "OS", "Hardware"], "answer": "Data format"},

    {"q": "What does GET method do?", "options": ["Retrieves data", "Deletes data", "Saves data", "Encrypts data"], "answer": "Retrieves data"},
    {"q": "What is a server?", "options": ["Host system", "User device", "Browser", "App"], "answer": "Host system"},
    {"q": "What is a client?", "options": ["User device", "Server", "Database", "Compiler"], "answer": "User device"},
    {"q": "What is SQL used for?", "options": ["Database queries", "Web design", "OS tasks", "Networking"], "answer": "Database queries"},
    {"q": "What is indentation in Python?", "options": ["Code structure", "Variable type", "Loop type", "File system"], "answer": "Code structure"},

    {"q": "What is a list in Python?", "options": ["Collection", "Loop", "Function", "Server"], "answer": "Collection"},
    {"q": "What is a dictionary?", "options": ["Key-value store", "Loop", "Function", "Class"], "answer": "Key-value store"},
    {"q": "What is a class?", "options": ["Blueprint", "Variable", "Loop", "File"], "answer": "Blueprint"},
    {"q": "What is an object?", "options": ["Instance of class", "Loop", "Function", "Server"], "answer": "Instance of class"},
    {"q": "What is inheritance?", "options": ["Code reuse", "Deletion", "Looping", "Compilation"], "answer": "Code reuse"},
]

# =========================
# SECTION B: CODE COMPLETION (25 QUESTIONS)
# =========================
CODE = [
    {"q": "Complete function: def add(a,b): return ____", "answer": "a+b"},
    {"q": "Fill loop: for i in range(5): print(____)", "answer": "i"},
    {"q": "Function keyword: ____", "answer": "def"},
    {"q": "Flask app creation: app = Flask(____)", "answer": "__name__"},
    {"q": "Condition: if x > 10: print(____)", "answer": "x"},

    {"q": "Loop type: while ____ < 10", "answer": "i"},
    {"q": "List syntax: mylist = [1, 2, ____]", "answer": "3"},
    {"q": "Dictionary key: {'name': 'John', ____: 20}", "answer": "age"},
    {"q": "Return keyword: ____ value", "answer": "return"},
    {"q": "Import module: ____ math", "answer": "import"},

    {"q": "Print function: ____('Hello')", "answer": "print"},
    {"q": "Input function: ____('Enter name')", "answer": "input"},
    {"q": "Loop counter: for i in ____", "answer": "range(10)"},
    {"q": "Comparison operator: x ____ y", "answer": ">"},
    {"q": "Equality operator: x ____ y", "answer": "=="},

    {"q": "Function call: add(2, ____)", "answer": "3"},
    {"q": "Boolean value: True or ____", "answer": "False"},
    {"q": "String type: ____", "answer": "str"},
    {"q": "Integer type: ____", "answer": "int"},
    {"q": "Float type: ____", "answer": "float"},

    {"q": "Loop keyword: ____ i in range(5)", "answer": "for"},
    {"q": "Condition keyword: ____ x > 5", "answer": "if"},
    {"q": "Else keyword: ____:", "answer": "else"},
    {"q": "Indentation defines ____", "answer": "block"},
    {"q": "Function output keyword: ____", "answer": "return"},
]

# =========================
# BUILD EXAM
# =========================
def generate_exam():
    exam = []

    for q in MCQ:
        exam.append({"type": "mcq", **q})

    for q in CODE:
        exam.append({"type": "code", **q})

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
            user = request.form.get(f"q{i}", "").strip()
            correct = q["answer"]

            mark = 2 if user.replace(" ", "").lower() == correct.replace(" ", "").lower() else 0
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