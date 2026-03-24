fastapi_template = """from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "Hello, World!"
"""

flask_template = """from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "Hello, World!"
"""

templates = {
    "fastapi": fastapi_template,
    "flask": flask_template,
}
