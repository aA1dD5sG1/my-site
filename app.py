from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

scan_count = 0
scan_history = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", scans=scan_count, history=scan_history)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    global scan_count, scan_history

    if request.method == 'POST':
        url = request.form.get("url")

        results = []
        status = "safe"

        scan_count += 1

        try:
            r = requests.get(url, timeout=5)
            headers = r.headers

            # فحص الهيدرز
            if "X-Frame-Options" not in headers:
                results.append("⚠️ Missing X-Frame-Options")
                status = "warning"

            if "Content-Security-Policy" not in headers:
                results.append("⚠️ Missing CSP")
                status = "warning"

            if "X-Content-Type-Options" not in headers:
                results.append("⚠️ Missing X-Content-Type-Options")
                status = "warning"

            # تحليل الصفحة
            soup = BeautifulSoup(r.text, "html.parser")
            forms = soup.find_all("form")

            if forms:
                results.append(f"ℹ️ Found {len(forms)} forms")

            if not results:
                results.append("✅ No obvious issues found")

        except:
            results.append("❌ Error scanning site")
            status = "danger"

        scan_history.append({
            "url": url,
            "status": status
        })

        return render_template("scan.html", results=results, target=url)

    return render_template("scan.html", results=None)


if __name__ == "__main__":
    app.run(debug=True)
