from flask import Flask, request, redirect, render_template
import requests
import logging
import os
from urllib.parse import urlparse

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

scan_history = []

@app.route('/')
def home():
    return render_template("index.html", history=scan_history)

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')

    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return "Invalid URL"

    report = []

    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        html = res.text.lower()

        # Security checks
        if "content-security-policy" not in headers:
            report.append("❌ Missing CSP")

        if "x-frame-options" not in headers:
            report.append("❌ Missing X-Frame-Options")

        if "x-content-type-options" not in headers:
            report.append("❌ Missing X-Content-Type-Options")

        if "strict-transport-security" not in headers:
            report.append("❌ Missing HSTS")

        if "<script>" in html:
            report.append("⚠️ Inline JS detected")

        if "password" in html:
            report.append("🔎 Login form detected")

        if not report:
            report.append("✅ No major issues")

    except Exception as e:
        report.append(f"Error: {e}")

    # حفظ في التاريخ
    scan_history.insert(0, {
        "url": url,
        "report": report
    })

    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
