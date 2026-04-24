from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# تخزين مؤقت للنتائج
scan_history = []

def scan_site(url):
    results = []

    try:
        start = time.time()
        res = requests.get(url, timeout=5)
        end = time.time()

        headers = res.headers

        # ===== Security Headers =====
        if "X-Frame-Options" not in headers:
            results.append(("⚠️ Missing X-Frame-Options", "medium"))

        if "Content-Security-Policy" not in headers:
            results.append(("⚠️ Missing Content-Security-Policy (CSP)", "high"))

        if "X-Content-Type-Options" not in headers:
            results.append(("⚠️ Missing X-Content-Type-Options", "low"))

        # ===== Basic Info =====
        results.append((f"🌐 Status Code: {res.status_code}", "info"))
        results.append((f"⏱ Response Time: {round(end-start,2)}s", "info"))

        # ===== HTML Analysis =====
        soup = BeautifulSoup(res.text, "html.parser")

        forms = soup.find_all("form")
        inputs = soup.find_all("input")
        links = soup.find_all("a")

        results.append((f"📄 Forms Found: {len(forms)}", "info"))
        results.append((f"🧾 Inputs Found: {len(inputs)}", "info"))
        results.append((f"🔗 Links Found: {len(links)}", "info"))

    except Exception as e:
        results.append((f"❌ Error: {str(e)}", "high"))

    return results


# ===== Routes =====

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "POST":
        url = request.form.get("url")

        if not url.startswith("http"):
            url = "http://" + url

        results = scan_site(url)

        # حفظ في history
        scan_history.append({
            "url": url,
            "count": len(results)
        })

        return render_template("scan.html", results=results, url=url)

    return render_template("scan.html", results=None)


@app.route("/dashboard")
def dashboard():
    total_scans = len(scan_history)
    return render_template("dashboard.html", history=scan_history, total=total_scans)


@app.route("/login")
def login():
    return render_template("login.html")


# ===== تشغيل =====
if __name__ == "__main__":
    app.run(debug=True)
