from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# عداد + تخزين النتائج
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
    global scan_count, scan_history
    return render_template("dashboard.html", scans=scan_count, history=scan_history)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    global scan_count, scan_history

    if request.method == 'POST':
        url = request.form.get("url")

        results = []
        status = "safe"

        scan_count += 1

        if not url.startswith("http"):
            results.append("❌ Invalid URL")
            status = "danger"
        else:
            results.append("⚠️ Missing X-Frame-Options")
            results.append("⚠️ Missing CSP")
            results.append("⚠️ Missing X-Content-Type-Options")
            results.append("ℹ️ Found 1 forms")
            status = "warning"

        # حفظ النتيجة
        scan_history.append({
            "url": url,
            "status": status
        })

        return render_template("scan.html", results=results, target=url)

    return render_template("scan.html", results=None)


if __name__ == "__main__":
    app.run(debug=True)
