from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

FIREBASE_API_KEY = os.environ.get(
    "FIREBASE_API_KEY",
    "AIzaSyCGzAuFIJrvud3hQoLm8SGgJTJx7M2NafM"
)


# =========================================================
# QUIZ QUESTIONS
# =========================================================

quiz_questions = {

    "python": [

        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["func", "def", "function", "define"],
            "answer": "def",
            "difficulty": "easy",
            "topic": "Functions"
        },

        {
            "question": "Which data type is used to store True or False?",
            "options": ["int", "str", "bool", "float"],
            "answer": "bool",
            "difficulty": "easy",
            "topic": "Data Types"
        },

        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#",
            "difficulty": "easy",
            "topic": "Basics"
        },

        {
            "question": "Which method adds an element to the end of a list?",
            "options": ["add()", "insert()", "append()", "push()"],
            "answer": "append()",
            "difficulty": "medium",
            "topic": "Lists"
        },

        {
            "question": "Which data structure stores key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary",
            "difficulty": "medium",
            "topic": "Data Structures"
        },

        {
            "question": "What is the output of len([10, 20, 30, 40])?",
            "options": ["3", "4", "5", "40"],
            "answer": "4",
            "difficulty": "medium",
            "topic": "Lists"
        },

        {
            "question": "Which keyword is used to handle exceptions?",
            "options": ["catch", "try", "error", "handle"],
            "answer": "try",
            "difficulty": "hard",
            "topic": "Exception Handling"
        },

        {
            "question": "What does list comprehension provide?",
            "options": [
                "A concise way to create lists",
                "A way to create classes",
                "A way to handle errors",
                "A way to import modules"
            ],
            "answer": "A concise way to create lists",
            "difficulty": "hard",
            "topic": "Lists"
        },

        {
            "question": "Which concept allows the same function name to behave differently based on objects?",
            "options": [
                "Encapsulation",
                "Polymorphism",
                "Compilation",
                "Iteration"
            ],
            "answer": "Polymorphism",
            "difficulty": "hard",
            "topic": "OOP"
        },

        {
            "question": "Which keyword creates an anonymous function in Python?",
            "options": [
                "anonymous",
                "lambda",
                "function",
                "inline"
            ],
            "answer": "lambda",
            "difficulty": "hard",
            "topic": "Functions"
        }
    ],


    "java": [

        {
            "question": "Which keyword is used to create a class in Java?",
            "options": ["class", "Class", "define", "struct"],
            "answer": "class",
            "difficulty": "easy",
            "topic": "Classes"
        },

        {
            "question": "Which method is the entry point of a Java program?",
            "options": ["start()", "main()", "run()", "execute()"],
            "answer": "main()",
            "difficulty": "easy",
            "topic": "Basics"
        },

        {
            "question": "Which keyword is used to inherit a class?",
            "options": [
                "inherits",
                "extends",
                "implements",
                "super"
            ],
            "answer": "extends",
            "difficulty": "easy",
            "topic": "Inheritance"
        },

        {
            "question": "Which data type stores whole numbers?",
            "options": [
                "float",
                "char",
                "int",
                "boolean"
            ],
            "answer": "int",
            "difficulty": "easy",
            "topic": "Data Types"
        },

        {
            "question": "Which keyword is used to create an object?",
            "options": [
                "object",
                "create",
                "new",
                "class"
            ],
            "answer": "new",
            "difficulty": "medium",
            "topic": "Objects"
        },

        {
            "question": "Which concept hides implementation details?",
            "options": [
                "Inheritance",
                "Abstraction",
                "Compilation",
                "Iteration"
            ],
            "answer": "Abstraction",
            "difficulty": "medium",
            "topic": "Abstraction"
        },

        {
            "question": "Which keyword is used to implement an interface?",
            "options": [
                "extends",
                "implements",
                "interface",
                "inherit"
            ],
            "answer": "implements",
            "difficulty": "medium",
            "topic": "Interfaces"
        },

        {
            "question": "Which OOP concept allows one method to have different implementations?",
            "options": [
                "Encapsulation",
                "Polymorphism",
                "Abstraction",
                "Inheritance"
            ],
            "answer": "Polymorphism",
            "difficulty": "hard",
            "topic": "Polymorphism"
        },

        {
            "question": "Which keyword refers to the current object?",
            "options": [
                "self",
                "current",
                "this",
                "object"
            ],
            "answer": "this",
            "difficulty": "hard",
            "topic": "Keywords"
        },

        {
            "question": "Which keyword refers to the immediate parent class?",
            "options": [
                "parent",
                "base",
                "super",
                "this"
            ],
            "answer": "super",
            "difficulty": "hard",
            "topic": "Inheritance"
        }
    ],


    "html": [

        {
            "question": "What does HTML stand for?",
            "options": [
                "Hyper Text Markup Language",
                "High Text Machine Language",
                "Hyperlink Text Markup Language",
                "Home Tool Markup Language"
            ],
            "answer": "Hyper Text Markup Language",
            "difficulty": "easy",
            "topic": "HTML Basics"
        },

        {
            "question": "Which tag is used to create a paragraph?",
            "options": [
                "<p>",
                "<para>",
                "<text>",
                "<paragraph>"
            ],
            "answer": "<p>",
            "difficulty": "easy",
            "topic": "HTML Tags"
        },

        {
            "question": "Which tag is used to create a hyperlink?",
            "options": [
                "<link>",
                "<a>",
                "<href>",
                "<url>"
            ],
            "answer": "<a>",
            "difficulty": "easy",
            "topic": "Links"
        },

        {
            "question": "Which tag is used to display an image?",
            "options": [
                "<image>",
                "<img>",
                "<picture>",
                "<src>"
            ],
            "answer": "<img>",
            "difficulty": "easy",
            "topic": "Images"
        },

        {
            "question": "Which attribute specifies the destination of a hyperlink?",
            "options": [
                "src",
                "link",
                "href",
                "target"
            ],
            "answer": "href",
            "difficulty": "medium",
            "topic": "Links"
        },

        {
            "question": "Which HTML element is used to create a table row?",
            "options": [
                "<td>",
                "<th>",
                "<tr>",
                "<row>"
            ],
            "answer": "<tr>",
            "difficulty": "medium",
            "topic": "Tables"
        },

        {
            "question": "Which tag is normally used for the largest heading?",
            "options": [
                "<h6>",
                "<head>",
                "<h1>",
                "<heading>"
            ],
            "answer": "<h1>",
            "difficulty": "medium",
            "topic": "Headings"
        },

        {
            "question": "Which attribute provides alternative text for an image?",
            "options": [
                "title",
                "alt",
                "text",
                "description"
            ],
            "answer": "alt",
            "difficulty": "hard",
            "topic": "Images"
        },

        {
            "question": "Which HTML element is used to collect user input?",
            "options": [
                "<input>",
                "<data>",
                "<collect>",
                "<user>"
            ],
            "answer": "<input>",
            "difficulty": "hard",
            "topic": "Forms"
        },

        {
            "question": "Which attribute is used to uniquely identify an HTML element?",
            "options": [
                "class",
                "name",
                "id",
                "unique"
            ],
            "answer": "id",
            "difficulty": "hard",
            "topic": "Attributes"
        }
    ],


    "dsa": [

        {
            "question": "Which data structure follows LIFO?",
            "options": [
                "Queue",
                "Stack",
                "Array",
                "Linked List"
            ],
            "answer": "Stack",
            "difficulty": "easy",
            "topic": "Stack"
        },

        {
            "question": "Which data structure follows FIFO?",
            "options": [
                "Stack",
                "Queue",
                "Tree",
                "Graph"
            ],
            "answer": "Queue",
            "difficulty": "easy",
            "topic": "Queue"
        },

        {
            "question": "Which data structure stores elements in contiguous memory locations?",
            "options": [
                "Array",
                "Tree",
                "Graph",
                "Stack"
            ],
            "answer": "Array",
            "difficulty": "easy",
            "topic": "Arrays"
        },

        {
            "question": "Which data structure consists of nodes connected using links?",
            "options": [
                "Array",
                "Linked List",
                "Stack",
                "Queue"
            ],
            "answer": "Linked List",
            "difficulty": "easy",
            "topic": "Linked List"
        },

        {
            "question": "What is the time complexity of accessing an array element by index?",
            "options": [
                "O(n)",
                "O(log n)",
                "O(1)",
                "O(n²)"
            ],
            "answer": "O(1)",
            "difficulty": "medium",
            "topic": "Arrays"
        },

        {
            "question": "Which searching algorithm requires a sorted array?",
            "options": [
                "Linear Search",
                "Binary Search",
                "Depth First Search",
                "Breadth First Search"
            ],
            "answer": "Binary Search",
            "difficulty": "medium",
            "topic": "Searching"
        },

        {
            "question": "What is the time complexity of binary search?",
            "options": [
                "O(n)",
                "O(n²)",
                "O(log n)",
                "O(1)"
            ],
            "answer": "O(log n)",
            "difficulty": "medium",
            "topic": "Searching"
        },

        {
            "question": "Which traversal uses a queue in a graph?",
            "options": [
                "DFS",
                "BFS",
                "Binary Search",
                "Merge Sort"
            ],
            "answer": "BFS",
            "difficulty": "hard",
            "topic": "Graphs"
        },

        {
            "question": "Which traversal commonly uses a stack or recursion?",
            "options": [
                "BFS",
                "DFS",
                "Binary Search",
                "Hashing"
            ],
            "answer": "DFS",
            "difficulty": "hard",
            "topic": "Graphs"
        },

        {
            "question": "What is the average-case search complexity of a hash table?",
            "options": [
                "O(n)",
                "O(log n)",
                "O(1)",
                "O(n²)"
            ],
            "answer": "O(1)",
            "difficulty": "hard",
            "topic": "Hashing"
        }
    ]
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match."

        try:

            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )

            db.collection("users").document(user.uid).set({
                "name": name,
                "email": email,
                "uid": user.uid
            })

            return redirect(url_for("login"))

        except Exception:

            app.logger.exception("Registration failed")

            return (
                "Registration failed. "
                "Please check your details and try again."
            )

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        try:

            login_url = (
                "https://identitytoolkit.googleapis.com/v1/"
                "accounts:signInWithPassword?key="
                + FIREBASE_API_KEY
            )

            response = requests.post(
                login_url,
                json={
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                },
                timeout=10
            )

            data = response.json()

            if response.status_code != 200:

                error_code = data.get(
                    "error",
                    {}
                ).get(
                    "message",
                    ""
                )

                credential_errors = {
                    "EMAIL_NOT_FOUND",
                    "INVALID_PASSWORD",
                    "INVALID_LOGIN_CREDENTIALS",
                    "USER_DISABLED"
                }

                if error_code in credential_errors:
                    error_message = "Invalid email or password."
                else:
                    error_message = (
                        "Firebase configuration error. "
                        "Please contact the administrator."
                    )

                return render_template(
                    "login.html",
                    error=error_message
                )

            id_token = data["idToken"]

            decoded_token = auth.verify_id_token(id_token)

            uid = decoded_token["uid"]

            user_record = auth.get_user(uid)

            session["uid"] = uid
            session["email"] = user_record.email
            session["name"] = user_record.display_name

            return redirect(url_for("dashboard"))

        except Exception:

            app.logger.exception("Firebase login verification failed")

            return render_template(
                "login.html",
                error=(
                    "Firebase configuration error. "
                    "Please contact the administrator."
                )
            )

    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "uid" not in session:
        return redirect(url_for("login"))

    uid = session["uid"]

    results = []

    for doc in db.collection("quiz_results").where(
        "uid",
        "==",
        uid
    ).stream():

        result = doc.to_dict()

        result["_created_at"] = doc.create_time
        result["_created_at_display"] = (
            doc.create_time.strftime(
                "%d %b %Y, %I:%M %p"
            )
            if doc.create_time
            else ""
        )

        results.append(result)

    quizzes_attempted = len(results)

    best_score = max(
        (
            r.get("percentage", 0)
            for r in results
        ),
        default=0
    )

    category_analysis = []

    for category in [
        "python",
        "java",
        "html",
        "dsa"
    ]:

        category_results = [
            result for result in results
            if result.get("category") == category
        ]

        if not category_results:
            continue

        latest_result = max(
            category_results,
            key=lambda result: result["_created_at"]
        )

        weak_topics = list(
            latest_result.get("weak_topics", [])
        )

        # Support older results that did not store weak_topics.
        if not weak_topics:

            for topic, stats in latest_result.get(
                "topic_stats",
                {}
            ).items():

                if stats.get("percentage", 0) <= 50:
                    weak_topics.append(topic)

        latest_score = latest_result.get(
            "percentage",
            0
        )

        if latest_score >= 80:
            recommendation = (
                "Great performance! Try harder questions next."
            )
        elif latest_score >= 50:
            recommendation = (
                "Good progress. Continue with medium-level practice."
            )
        else:
            recommendation = (
                "You need more practice. Try easier questions first."
            )

        category_analysis.append({
            "category": category,
            "recommendation": recommendation,
            "weak_topics": weak_topics
        })

    return render_template(
        "dashboard.html",
        name=session.get("name"),
        quizzes_attempted=quizzes_attempted,
        best_score=best_score,
        category_analysis=category_analysis
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    if "uid" not in session:
        return redirect(url_for("login"))

    results = []

    for doc in db.collection("quiz_results").where(
        "uid",
        "==",
        session["uid"]
    ).stream():

        result = doc.to_dict()

        result["_created_at"] = doc.create_time

        result["_created_at_display"] = (
            doc.create_time.strftime(
                "%d %b %Y, %I:%M %p"
            )
            if doc.create_time
            else ""
        )

        results.append(result)

    # Latest result first
    results.sort(
        key=lambda x: x.get("_created_at"),
        reverse=True
    )

    return render_template(
        "history.html",
        results=results
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================================================
# CATEGORIES
# =========================================================

@app.route("/categories")
def categories():

    if "uid" not in session:
        return redirect(url_for("login"))

    return render_template("categories.html")


# =========================================================
# WEAK TOPIC ANALYSIS
# =========================================================

def analyze_weak_topics(category, answers, quiz_data):

    topic_stats = {}

    for i, question in enumerate(quiz_data):

        topic = question.get(
            "topic",
            "General"
        )

        if topic not in topic_stats:

            topic_stats[topic] = {
                "correct": 0,
                "total": 0
            }

        topic_stats[topic]["total"] += 1

        user_answer = answers.get(
            str(i)
        )

        if user_answer == question["answer"]:

            topic_stats[topic]["correct"] += 1

    weak_topics = []

    for topic, stats in topic_stats.items():

        total = stats["total"]

        correct = stats["correct"]

        percentage = (
            round((correct / total) * 100)
            if total > 0
            else 0
        )

        stats["percentage"] = percentage

        # 50% or below = weak topic
        if percentage <= 50:

            weak_topics.append(topic)

    return topic_stats, weak_topics


# =========================================================
# ADAPTIVE QUESTION SELECTION
# =========================================================

def get_adaptive_questions(category):

    quiz_data = quiz_questions[category]

    target_difficulty = "medium"

    weak_topics = []

    uid = session.get("uid")

    if uid:

        previous_results = list(
            db.collection("quiz_results")
            .where("uid", "==", uid)
            .where("category", "==", category)
            .stream()
        )

        # Sort results by creation time
        previous_results.sort(
            key=lambda doc: doc.create_time
        )

        if previous_results:

            latest_result = (
                previous_results[-1].to_dict()
            )

            latest_score = latest_result.get(
                "percentage",
                0
            )

            weak_topics = latest_result.get(
                "weak_topics",
                []
            )

            # Adaptive difficulty
            if latest_score >= 80:

                target_difficulty = "hard"

            elif latest_score >= 50:

                target_difficulty = "medium"

            else:

                target_difficulty = "easy"

    # -----------------------------------------------------
    # First priority: weak topic questions
    # -----------------------------------------------------

    weak_topic_questions = [

        q for q in quiz_data

        if q.get("topic") in weak_topics
    ]

    # -----------------------------------------------------
    # Second priority: target difficulty
    # -----------------------------------------------------

    target_questions = [

        q for q in quiz_data

        if q.get("difficulty") == target_difficulty

        and q not in weak_topic_questions
    ]

    # -----------------------------------------------------
    # Remaining questions
    # -----------------------------------------------------

    other_questions = [

        q for q in quiz_data

        if q not in weak_topic_questions

        and q not in target_questions
    ]

    # Weak topics first,
    # then adaptive difficulty,
    # then remaining questions

    return (
        weak_topic_questions
        + target_questions
        + other_questions
    )


# =========================================================
# SAVE QUIZ RESULT
# =========================================================

def save_quiz_result(category, quiz_data, answers):

    score = sum(

        1

        for i, question in enumerate(quiz_data)

        if answers.get(str(i))
        == question["answer"]
    )

    total = len(quiz_data)

    percentage = (
        round((score / total) * 100)
        if total
        else 0
    )

    # Analyze topic performance
    topic_stats, weak_topics = analyze_weak_topics(
        category,
        answers,
        quiz_data
    )

    # Save result to Firestore
    db.collection("quiz_results").add({

        "uid": session["uid"],

        "email": session["email"],

        "category": category,

        "score": score,

        "total": total,

        "percentage": percentage,

        "topic_stats": topic_stats,

        "weak_topics": weak_topics,

        "created_at": firestore.SERVER_TIMESTAMP
    })

    # Store result temporarily in session
    session["score"] = score

    session["total"] = total

    session["percentage"] = percentage

    session["result_category"] = category

    return score, total, percentage


# =========================================================
# QUIZ
# =========================================================

@app.route(
    "/quiz/<category>/<int:number>",
    methods=["GET", "POST"]
)
def quiz(category, number):

    if "uid" not in session:
        return redirect(url_for("login"))

    if category not in quiz_questions:
        return "Invalid category."

    # -----------------------------------------------------
    # Start new quiz
    # -----------------------------------------------------

    if number == 0 and request.method == "GET":

        session["answers"] = {}

        for key in [
            "score",
            "total",
            "percentage",
            "result_category"
        ]:
            session.pop(key, None)

        session["adaptive_questions"] = (
            get_adaptive_questions(category)
        )

        session["adaptive_category"] = category

    quiz_data = (
        session.get("adaptive_questions")
        if session.get("adaptive_category") == category
        else quiz_questions[category]
    )

    session["adaptive_questions"] = quiz_data

    # -----------------------------------------------------
    # Validate question number
    # -----------------------------------------------------

    if number < 0:

        number = 0

    if number >= len(quiz_data):

        return redirect(
            url_for(
                "result",
                category=category
            )
        )

    # -----------------------------------------------------
    # Start 60 second timer
    # -----------------------------------------------------

    if request.method == "GET":

        session["quiz_start_time"] = time.time()

    if "quiz_start_time" in session:

        remaining_time = max(
            0,
            int(
                60
                - (
                    time.time()
                    - session["quiz_start_time"]
                )
            )
        )

    else:

        remaining_time = 60

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        selected_answer = request.form.get(
            "answer"
        )

        action = request.form.get(
            "action"
        )

        answers = session.get(
            "answers",
            {}
        )

        # Save selected answer
        if selected_answer:

            answers[str(number)] = (
                selected_answer
            )

        session["answers"] = answers

        # -------------------------------------------------
        # Previous
        # -------------------------------------------------

        if action == "previous":

            return redirect(
                url_for(
                    "quiz",
                    category=category,
                    number=max(
                        0,
                        number - 1
                    )
                )
            )

        # -------------------------------------------------
        # Next
        # -------------------------------------------------

        if (
            action == "next"
            and number < len(quiz_data) - 1
        ):

            return redirect(
                url_for(
                    "quiz",
                    category=category,
                    number=number + 1
                )
            )

        # -------------------------------------------------
        # Submit
        # -------------------------------------------------

        if action == "submit":

            save_quiz_result(
                category,
                quiz_data,
                answers
            )

            for key in [
                "quiz_start_time",
                "adaptive_questions",
                "adaptive_category",
                "answers"
            ]:

                session.pop(
                    key,
                    None
                )

            return redirect(
                url_for(
                    "result",
                    category=category
                )
            )

    # -----------------------------------------------------
    # Auto submit after 60 seconds
    # -----------------------------------------------------

    if (
        "quiz_start_time" in session
        and
        time.time()
        - session["quiz_start_time"]
        >= 60
    ):

        answers = session.get(
            "answers",
            {}
        )

        save_quiz_result(
            category,
            quiz_data,
            answers
        )

        for key in [
            "quiz_start_time",
            "adaptive_questions",
            "adaptive_category",
            "answers"
        ]:

            session.pop(
                key,
                None
            )

        return redirect(
            url_for(
                "result",
                category=category
            )
        )

    # -----------------------------------------------------
    # Current question
    # -----------------------------------------------------

    question = quiz_data[number]

    answers = session.get(
        "answers",
        {}
    )

    selected_answer = answers.get(
        str(number)
    )

    return render_template(
        "quiz.html",

        question=question["question"],

        options=question["options"],

        question_number=number + 1,

        total_questions=len(quiz_data),

        selected_answer=selected_answer,

        category=category,

        current_number=number,

        remaining_time=remaining_time
    )


# =========================================================
# RESULT
# =========================================================

@app.route("/result/<category>")
def result(category):

    if "uid" not in session:
        return redirect(url_for("login"))

    score = session.get(
        "score",
        0
    )

    total = session.get(
        "total",
        len(
            quiz_questions.get(
                category,
                []
            )
        )
    )

    percentage = session.get(
        "percentage",
        round(
            (score / total) * 100
        ) if total else 0
    )

    if session.get("result_category") != category:
        return redirect(url_for("categories"))

    return render_template(
        "result.html",

        score=score,

        total=total,

        percentage=percentage,

        category=category
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=False
    )