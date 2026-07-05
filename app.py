import os
import socket
from datetime import datetime
from flask import Flask

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "Version 3")
HOSTNAME = socket.gethostname()


@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>☕ Chai Politics</title>

    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #f4f6f9;
            font-family: Arial, Helvetica, sans-serif;
        }}

        .container {{
            width: 800px;
            margin: 40px auto;
        }}

        .header {{
            background: #8B4513;
            color: white;
            padding: 20px;
            border-radius: 10px 10px 0 0;
        }}

        .content {{
            background: white;
            padding: 25px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0px 4px 15px rgba(0,0,0,.15);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th {{
            background: #eeeeee;
            text-align: left;
            padding: 12px;
            width: 35%;
        }}

        td {{
            padding: 12px;
        }}

        tr:nth-child(even) {{
            background: #f9f9f9;
        }}

        .status {{
            margin-top: 25px;
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 6px;
            font-weight: bold;
        }}

        .footer {{
            margin-top: 25px;
            text-align: center;
            color: gray;
            font-size: 14px;
        }}

        h1 {{
            margin: 0;
        }}
    </style>

</head>

<body>

<div class="container">

<div class="header">
<h1>☕ Chai Politics</h1>
<p>Google Kubernetes Engine CI/CD Demo</p>
</div>

<div class="content">

<h2>Application Information</h2>

<table>

<tr>
<th>Application</th>
<td>Chai Politics</td>
</tr>

<tr>
<th>Environment</th>
<td>Production</td>
</tr>

<tr>
<th>Version</th>
<td>{VERSION}</td>
</tr>

<tr>
<th>Pod Name</th>
<td>{HOSTNAME}</td>
</tr>

<tr>
<th>Current Time</th>
<td>{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</td>
</tr>

<tr>
<th>Container Port</th>
<td>8080</td>
</tr>

<tr>
<th>Platform</th>
<td>Google Kubernetes Engine (GKE)</td>
</tr>

<tr>
<th>CI/CD</th>
<td>Cloud Build → Artifact Registry → GKE</td>
</tr>

<tr>
<th>Developer</th>
<td>Ankit Raj</td>
</tr>

</table>

<div class="status">
✅ Application is running successfully on Kubernetes.
</div>

<div class="footer">
Built with ❤️ using Flask, Docker, Cloud Build and GKE
</div>

</div>

</div>

</body>
</html>
"""


@app.route("/health")
def health():
    return {
        "status": "UP",
        "application": "chai-politics",
        "version": VERSION,
        "pod": HOSTNAME
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)