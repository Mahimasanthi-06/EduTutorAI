from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from google import genai
import sqlite3
import os
import markdown
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


app = Flask(__name__)

pdf_content = ""
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
DATABASE = "database/database.db"
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO students(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@app.route("/upload", methods=["GET", "POST"])
def upload():

    global pdf_content

    if request.method == "POST":

        file = request.files["pdf"]

        if file:

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)


            # Read PDF
            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted


            # Store PDF content
            pdf_content = text


            return render_template(
                "pdf_text.html",
                text=text
            )

    return render_template("upload.html")



# 👇 PASTE THE NEW ASK_AI FUNCTION HERE

@app.route("/ask_ai", methods=["GET", "POST"])
def ask_ai():

    global pdf_content

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        if pdf_content.strip():

            prompt = f"""
You are EduTutorAI, an intelligent AI tutor.

The student has uploaded study notes.

Use the notes as the main source when answering.

Study Notes:
{pdf_content}

Student Question:
{question}

Give a clear and easy-to-understand answer.
Use headings, bullet points and examples when useful.
"""

        else:

            prompt = f"""
You are EduTutorAI, an intelligent AI tutor.

The student has NOT uploaded any study notes.

Answer the student's question using your general knowledge.

Student Question:
{question}

Give a clear and easy-to-understand answer.
Use headings, bullet points and examples when useful.
"""

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            answer = markdown.markdown(response.text, extensions=["extra"])

        except Exception as e:

            answer = f"Gemini Error: {str(e)}"

    return render_template(
        "ask_ai.html",
        answer=answer
    )



@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    quiz = ""

    if request.method == "POST":

        topic = request.form["topic"]


        prompt = f"""
You are an AI Tutor.

Generate a quiz from these study notes.

Notes:
{pdf_content}


Topic:
{topic}


Create:
- 5 Multiple Choice Questions
- 4 options each
- Give answers at the end
"""


        try:
            response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
)
            quiz = response.text
        except Exception as e:

            quiz = str(e)


    return render_template(
        "quiz.html",
        quiz=quiz
    )
@app.route("/planner", methods=["GET", "POST"])
def planner():

    plan = ""

    if request.method == "POST":

        subject = request.form["subject"]

        plan = f"""
📅 Study Plan for {subject}

Day 1 : Learn Basics

Day 2 : Practice Examples

Day 3 : Solve Problems

Day 4 : Revise Notes

Day 5 : Take Mock Test
"""

    return render_template("planner.html", plan=plan)
@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)