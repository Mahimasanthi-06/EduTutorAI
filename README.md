# 🎓 EduTutor AI

EduTutor AI is a Flask-based Generative AI learning platform designed to help students study using AI-powered assistance.

Students can upload study notes in PDF format, ask questions about their notes, generate quizzes, and create study plans through a simple web interface.

## 🚀 Features

* 📄 Upload PDF study notes
* 🤖 AI Tutor using Google Gemini
* 📝 AI-powered quiz generation
* 📅 Study planner
* 🔐 Student registration and login
* 🗄️ SQLite database for student information
* 📚 PDF text extraction using PyPDF2
* 🎨 Simple responsive web interface using Bootstrap

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* SQLite

### Generative AI

* Google Gemini API
* `google-genai`

### PDF Processing

* PyPDF2

### Frontend

* HTML
* CSS
* Bootstrap

### Other Python Libraries

* python-dotenv
* Markdown
* Werkzeug

## 🏗️ Project Structure

```text
EduTutorAI/
│
├── app.py
├── create_db.py
├── database/
│   └── database.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── pdf_text.html
│   ├── ask_ai.html
│   ├── quiz.html
│   └── planner.html
│
├── uploads/
│   └── uploaded PDF files
│
├── .env
├── .gitignore
└── README.md
```

## 🔄 How the Application Works

```text
Student
   ↓
Home Page
   ↓
Register / Login
   ↓
Dashboard
   ↓
Choose a feature
```

The dashboard provides four main features:

```text
                 EduTutor AI
                      |
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   Upload PDF     AI Tutor       Quiz Generator
        ↓             ↓             ↓
   PyPDF2         Gemini API     Gemini API
        ↓             ↓             ↓
   Extract text   AI Answer      Quiz
        |
   pdf_content
        |
        └──────────→ AI Tutor / Quiz
```

## 📄 1. PDF Upload

The student selects a PDF containing study material.

The Flask server receives the file and saves it in the `uploads` folder.

PyPDF2 then reads the PDF page by page and extracts the text.

The extracted text is temporarily stored in the application as `pdf_content`.

### Flow

```text
PDF
 ↓
Flask
 ↓
Save file
 ↓
PyPDF2
 ↓
Extract text
 ↓
pdf_content
```

## 🤖 2. AI Tutor

The AI Tutor allows students to ask questions.

### When a PDF is uploaded

The application sends the uploaded study material together with the student's question to Gemini.

```text
Study Notes
     +
Student Question
     ↓
Prompt
     ↓
Gemini API
     ↓
Generated Answer
```

The prompt instructs Gemini to use the study notes as the main source and provide an easy-to-understand response with headings, bullet points and examples.

### When no PDF is uploaded

The application sends the student's question to Gemini and asks it to answer using general knowledge.

Therefore, the AI Tutor supports both:

* PDF-based question answering
* General AI question answering

## 📝 3. Quiz Generator

The student enters a topic.

The application creates a prompt for Gemini containing the study notes and requested topic.

Gemini generates:

* 5 multiple-choice questions
* 4 options for each question
* Answers at the end

### Flow

```text
Topic
  +
Study Notes
  ↓
Prompt
  ↓
Gemini API
  ↓
5 MCQs
  ↓
Quiz Page
```

## 📅 4. Study Planner

The student enters a subject.

The current version creates a simple five-day study plan:

```text
Day 1 → Learn Basics
Day 2 → Practice Examples
Day 3 → Solve Problems
Day 4 → Revise Notes
Day 5 → Take Mock Test
```

The current Study Planner uses Python logic rather than Gemini.

## 🔐 5. Registration and Login

Students can create an account using:

* Name
* Email
* Password

The information is stored in an SQLite database.

```text
Registration
     ↓
SQLite
     ↓
students table
```

During login, the application checks the entered email and password against the database.

## 🗄️ Database

The project uses SQLite.

The `students` table contains:

| Column   | Purpose           |
| -------- | ----------------- |
| id       | Unique student ID |
| name     | Student name      |
| email    | Student email     |
| password | Student password  |

The database is created using `create_db.py`.

## 🧠 Generative AI Workflow

The main Generative AI workflow is:

```text
Student Question
       ↓
Flask Application
       ↓
Build Prompt
       ↓
Google Gemini API
       ↓
Gemini Generates Response
       ↓
Flask Receives Response
       ↓
HTML Page
       ↓
Student
```

For PDF-based questions:

```text
PDF
 ↓
PyPDF2
 ↓
Extracted Text
 ↓
Prompt + Student Question
 ↓
Gemini
 ↓
AI Answer
```

## 🔑 Environment Variables

The Gemini API key is stored in a local `.env` file.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit the real API key to GitHub.

The `.env` file should be included in `.gitignore`.

## ▶️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Mahimasanthi-06/EduTutorAI.git
cd EduTutorAI
```

### 2. Create a virtual environment

```bash
py -3.12 -m venv venv
```

### 3. Activate the virtual environment on Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install flask python-dotenv google-genai PyPDF2 markdown
```

### 5. Configure the Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

### 6. Create the database

```bash
python create_db.py
```

### 7. Run the Flask application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 📌 Example User Flow

```text
1. Open EduTutor AI
       ↓
2. Register
       ↓
3. Login
       ↓
4. Open Dashboard
       ↓
5. Upload study PDF
       ↓
6. PDF text is extracted
       ↓
7. Open AI Tutor
       ↓
8. Ask a question
       ↓
9. Gemini generates an answer
       ↓
10. Generate a quiz from the topic
       ↓
11. Create a study plan
```

## 🎯 Project Objective

The goal of EduTutor AI is to provide students with a simple AI-assisted learning platform where study material, question answering, quiz generation and study planning are available in one application.

## 🔮 Future Improvements

Possible future improvements include:

* Password hashing
* Flask sessions and protected routes
* Persistent student-specific PDF storage
* Better PDF processing
* RAG-based document retrieval
* Personalized AI study plans
* Quiz scoring
* Student progress tracking
* Database storage for quiz results
* Multiple PDF support
* Deployment to a cloud platform
* Improved authentication and security
* Chat history

## 👩‍💻 Project Type

**Generative AI + Web Application**

Built using:

**Python + Flask + Google Gemini + SQLite + PyPDF2 + HTML/CSS/Bootstrap**
