# STUDENT COURSE API

A small, read-only REST API built with **Python + Flask**, created for
**System Integration and Architecture - Laboratory Activity 3A**.

It serves six fictional university courses kept directly in the source code.
There is **no database**, **no authentication**, and **no create / update / delete**.

Live endpoints after deployment:

| Method | Route | Purpose |
| ------ | ----- | ------- |
| GET | `/api/health` | Check that the server is running |
| GET | `/api/courses` | List all available courses |
| GET | `/api/courses/<id>` | Get one course by its integer ID |

---

## 1. Important note about Base44

This project was planned in Base44, but **Base44 does not run Python or Flask**.
Its managed backend runs JavaScript / TypeScript server code, so the Flask app
cannot be hosted there and must never be described as running on Base44.

The three files in this folder are a **standalone Flask project**. They do not
import anything from Base44 and they run on any computer with Python installed,
and on Render, exactly as described below.

---

## 2. Technology stack

- **Python 3** - the programming language
- **Flask** - the micro web framework that handles routes and JSON responses
- **Flask-Cors** - allows a browser app on another origin to call the API
- **Gunicorn** - the production web server that runs Flask on Render
- **GitHub** - stores the source code
- **Render** - hosts the public API as a Web Service

---

## 3. Project structure

```
student-course-api/
├── app.py             # Flask application, sample data, routes, error handling
├── requirements.txt   # Python dependencies
├── README.md          # This documentation
└── .gitignore         # Files Git should not upload (optional but recommended)
```

---

## 4. Installation

1. Install Python 3.8 or newer from https://www.python.org/downloads/
   (on Windows, tick **Add Python to PATH** during installation).
2. Open a terminal inside the project folder.
3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate it:

   Windows:

   ```
   venv\Scripts\activate
   ```

   macOS / Linux:

   ```
   source venv/bin/activate
   ```

5. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

---

## 5. Run the API on your own computer

```
python app.py
```

You should see Flask report that it is running on `http://127.0.0.1:5000`.
Open that address in a browser - the root path answers with a JSON 404 by
design, because only the three `/api/...` routes are defined.

Stop the server with `Ctrl + C`.

---

## 6. API documentation

### A. GET /api/health

Verifies that the backend is operating.

Request:

```
GET http://127.0.0.1:5000/api/health
```

Response - HTTP **200 OK**:

```json
{
  "status": "success",
  "message": "Student Course API is running"
}
```

### B. GET /api/courses

Returns every course as a JSON array.

Request:

```
GET http://127.0.0.1:5000/api/courses
```

Response - HTTP **200 OK** (shortened):

```json
[
  {
    "id": 1,
    "code": "CS 101",
    "name": "Introduction to Programming",
    "units": 3,
    "description": "Build your first programs with variables, loops, and functions in Python."
  },
  {
    "id": 2,
    "code": "IT 204",
    "name": "Database Management Systems",
    "units": 3,
    "description": "Design tables, write SQL queries, and normalize a small school database."
  }
]
```

### C. GET /api/courses/<id>

Returns one course whose integer `id` matches.

Request:

```
GET http://127.0.0.1:5000/api/courses/3
```

Response - HTTP **200 OK**:

```json
{
  "id": 3,
  "code": "IS 310",
  "name": "Systems Integration and Architecture",
  "units": 3,
  "description": "Connect separate services and compare API styles such as REST and SOAP."
}
```

Request for a course that does not exist:

```
GET http://127.0.0.1:5000/api/courses/99
```

Response - HTTP **404 Not Found**:

```json
{
  "status": "error",
  "message": "Course with ID 99 was not found.",
  "available_ids": [1, 2, 3, 4, 5, 6]
}
```

Any other method (POST, PUT, DELETE) on these routes answers **405** with a JSON
message saying the API is read-only.

---

## 7. Testing the API

### Browser

Open each address directly. Chrome, Edge, and Firefox display the JSON, and the
**Network** tab of the developer tools shows the HTTP status code.

### curl (macOS, Linux, Git Bash)

```
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/courses
curl -i http://127.0.0.1:5000/api/courses/3
curl -i http://127.0.0.1:5000/api/courses/99
```

`-i` shows the status line, so you can confirm **200** versus **404**.

### PowerShell (Windows)

```
Invoke-RestMethod http://127.0.0.1:5000/api/health
Invoke-RestMethod http://127.0.0.1:5000/api/courses
```

### Postman

1. Create a new request and choose **GET**.
2. Paste the URL, for example `http://127.0.0.1:5000/api/courses/3`.
3. Press **Send** and read the status code and the JSON body.

### What "tested" means

Only mark an endpoint as tested after you have actually sent the request and seen
the response. A screenshot of the JSON plus the status code is good evidence for
your submission.

---

## 8. Upload the project to GitHub

1. Create the repository on https://github.com/new (name it
   `student-course-api`, keep it **Public**, do not add a README).
2. Create a `.gitignore` file in the project folder:

   ```
   venv/
   __pycache__/
   *.pyc
   .env
   ```

3. In the project folder run:

   ```
   git init
   git add .
   git commit -m "Add Student Course API for Laboratory Activity 3A"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/student-course-api.git
   git push -u origin main
   ```

4. Refresh the repository page and confirm that `app.py`,
   `requirements.txt`, and `README.md` are visible.

Never upload your virtual environment folder - it is large and machine specific.

---

## 9. Deploy to Render

1. Sign in at https://render.com with your GitHub account.
2. Click **New +** then **Web Service**.
3. Choose **Build and deploy from a Git repository** and connect
   `student-course-api`.
4. Fill in the service settings:

   | Setting | Value |
   | ------- | ----- |
   | Name | `student-course-api` |
   | Language / Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:app` |
   | Instance Type | Free |

5. Leave the environment variables empty. Render sets `PORT` automatically and
   `app.py` already reads it. (Optional: add `PYTHON_VERSION` with `3.11.9`.)
6. Click **Create Web Service** and wait for the log to say
   `Your service is live`.
7. Copy the public URL, for example
   `https://student-course-api.onrender.com`.

### Why `gunicorn app:app` works

`gunicorn` is the server, `app` before the colon is the **file** `app.py`, and
`app` after the colon is the **Flask object** inside that file. If you rename
either one, the start command must change with it.

### Testing the public URL

```
https://student-course-api.onrender.com/api/health
https://student-course-api.onrender.com/api/courses
https://student-course-api.onrender.com/api/courses/1
https://student-course-api.onrender.com/api/courses/99
```

Free Render services sleep after a period without traffic, so the first request
may take 30-60 seconds. That is normal.

---

## 10. Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies are not installed. Run `pip install -r requirements.txt` in the active virtual environment. |
| `Error: Could not import 'app'` on Render | `app.py` is not in the repository root, or the Flask object is not named `app`. |
| Render build fails | Check the Build Command is exactly `pip install -r requirements.txt`. |
| Port already in use locally | Another program uses 5000. Set a different port, e.g. `set PORT=5001` before `python app.py`. |
| Browser shows HTML instead of JSON | You opened a route other than `/api/...`. The JSON 404 body confirms the server is alive. |

---

## 11. Beginner learning guide

**What is a REST API?**
A REST API is a set of URLs a program can call to read or change data. Each URL
is a *resource* and each HTTP method is an *action*. This project only reads, so
it uses only GET.

**What do Python and Flask do?**
Python is the language; Flask is a small framework that turns a Python function
into a URL. Without Flask you would have to parse HTTP yourself.

**What is `app.py` for?**
It creates the application object, defines the sample data, maps each URL to a
function, and configures the server.

**What is `requirements.txt` for?**
It lists the libraries the project needs with pinned versions. Anyone, or any
server such as Render, can install the same environment with one command.

**What is `README.md` for?**
It documents the project so another person can install, run, test, and deploy it
without asking you.

**What is a GET request?**
A GET request asks the server for data and must never change anything. That is
why this API is read-only and safe to refresh.

**How do the three endpoints work?**
`/api/health` returns a fixed message, proving the server runs.
`/api/courses` returns the whole list.
`/api/courses/<id>` searches the list for a matching `id` and returns one
course, or a 404 error when nothing matches.

**How are JSON responses structured?**
`jsonify()` converts a Python dictionary or list into a JSON body and sets the
`Content-Type: application/json` header. Objects use `{ }` with `"key": value`
pairs; arrays use `[ ]`.

**HTTP 200 versus HTTP 404**
200 means the request succeeded. 404 means the thing you asked for does not
exist. The status code is how a program understands the result without reading
the text.

**Running it locally**
Create the virtual environment, install the requirements, run `python app.py`,
and open `http://127.0.0.1:5000/api/health`.

**Testing it**
Open the routes in a browser, or send them with curl or Postman, and read both
the JSON body and the status code.

**GitHub**
Commit the three files, add the GitHub URL as `origin`, and push to `main`.
The repository is your submission and the source Render reads.

**Connecting Render**
Create a Web Service from that repository, set the Build Command to
`pip install -r requirements.txt` and the Start Command to `gunicorn app:app`.

**Deploying**
Press **Create Web Service** and watch the log until the service is live. Every
future `git push` redeploys automatically.

**Testing the public URL**
Replace `127.0.0.1:5000` with your Render URL and repeat the same four test
requests: health, all courses, one course, and a missing id.

---

## 12. Validation checklist

- [x] Standalone Python Flask application
- [x] `GET /api/health` returns 200 with the required JSON
- [x] `GET /api/courses` returns a JSON array of six courses
- [x] `GET /api/courses/<id>` returns one course or a 404 error
- [x] Six fictional course records stored in the source code
- [x] Valid JSON for every response, including errors
- [x] Correct HTTP status codes (200 / 404 / 405 / 500)
- [x] GET-only, read-only API
- [x] CORS enabled for a classroom demonstration
- [x] No authentication
- [x] No database connection
- [x] `app.py`, `requirements.txt`, `README.md` included
- [x] Gunicorn compatible (`app:app`)
- [x] Render-compatible configuration (`0.0.0.0`, `PORT`)

Items marked [x] were confirmed by reading the source and by executing the
routes on Python 3.11. The three items below need your own accounts:

- [ ] Repository pushed to your GitHub account
- [ ] Web Service created on your Render account
- [ ] Public URL answering all four test requests
