fastapi_template = """\
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}
"""

flask_template = """\
from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello_world():
    return {"status": "ok"}
"""

gitignore_template = """\
# Python-generated files
__pycache__/
.venv/
build/
dist/
*.egg-info/
*.py[cod]

# Secrets
.env

# Databases
*.sqlite
*.db

# OS-generated
.DS_Store
Thumbs.db
"""

templates = {
    "fastapi": fastapi_template,
    "flask": flask_template,
    "gitignore": gitignore_template,
}
