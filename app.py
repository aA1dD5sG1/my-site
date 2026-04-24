from flask import Flask, request, render_template_string
import logging
import re

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# كلمات/أنماط مشبوهة
xss_patterns = ["<script>", "onerror", "alert(", "<img", "<svg"]
sql_patterns = ["' OR", "'--", "UNION", "SELECT", "DROP", "--"]

def detect_attack(data):
    data = data.lower()
    
    for x in xss_patterns:
        if x.lower() in data:
            return "XSS Attempt"
    
    for s in sql_patterns:
        if s.lower() in data:
            return "SQL Injection Attempt"
    
    return None

@app.before_request
def monitor():
    ip = request.remote_addr
    url = request.url
    data = request.get_data(as_text=True)

    attack = detect_attack(data)

    app.logger.info(f"IP: {ip}")
    app.logger.info(f"URL: {url}")
    app.logger.info(f"DATA: {data}")

    if attack:
        app.logger.warning(f"⚠️ {attack} from {ip}")

@app.route("/")
def home():
    return """
    <h2>Test Page</h2>
    <form method="POST" action="/test">
        <input name="input" placeholder="Try attack here">
        <button type="submit">Send</button>
    </form>
    """

@app.route("/test", methods=["POST"])
def test():
    user_input = request.form.get("input")
    return f"You entered: {user_input}"

app.run()
