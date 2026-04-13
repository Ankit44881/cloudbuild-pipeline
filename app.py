import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello from Ankit's CI-CD."

if __name__ == "__main__":
    # Cloud Run/GCP expects the app to listen on the port defined by the PORT env var
    # Defaulting to 8080 if not set locally
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)