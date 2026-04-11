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

templates = {
    "fastapi": fastapi_template,
    "flask": flask_template,
}
