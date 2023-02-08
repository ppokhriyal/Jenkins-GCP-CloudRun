from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Welcome to GCP CI-CD : Jenkins -> Docker Image -> GCP Artifact -> Cloud Run</h1>"
