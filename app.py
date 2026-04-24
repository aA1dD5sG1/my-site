from flask import Flask, render_template, request, redirect, session
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

app = Flask(__name__)
app.secret_key = "secret123"

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        result TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# 🏠 الصفحة الرئيسية
@app.route("/")
def index():
    return redirect("/login")

# 🔐 تسجيل الدخول
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("LOGIN:", username, password)

        session["user"] = username
        return redirect("/dashboard")

    return render_template("login.html")

# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scans ORDER BY id DESC")
    scans = c.fetchall()
    conn.close()

    return render_template("dashboard.html", scans=scans)

# 🧠 Scanner
def scan_website(url):
    results = []

    try:
        res = requests.get(url, timeout=5)
        headers = res.headers

        # Headers
        if "X-Frame-Options" not in headers:
            results.append("⚠️ Missing X-Frame-Options")

        if "Content-Security-Policy" not in headers:
            results.append("⚠️ Missing CSP")

        if "X-Content-Type-Options" not in headers:
            results.append("⚠️ Missing X-Content-Type-Options")

        # تحليل الصفحة
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        if forms:
            results.append(f"ℹ️ Found {len(forms)} forms")

        # اختبار XSS بسيط
        payload = "<script>alert(1)</script>"
        test_url = url + "?test=" + payload

        test_res = requests.get(test_url)

        if payload in test_res.text:
            results.append("🚨 Possible XSS")

        if not results:
            results.append("✅ No major issues")

    except Exception as e:
        results.append(f"❌ Error: {e}")

    return results

# 🔍 Route الفحص (محسّن)
@app.route("/scan", methods=["GET", "POST"])
def scan():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        url = request.form.get("url")

        if not url.startswith("http"):
            url = "http://" + url

        parsed = urlparse(url)
        if not parsed.netloc:
            return render_template("scan.html", error="Invalid URL")

        results = scan_website(url)

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO scans (url, result, date) VALUES (?, ?, ?)",
            (url, " | ".join(results), str(datetime.datetime.now()))
        )
        conn.commit()
        conn.close()

        return render_template("scan.html", results=results, target=url)

    return render_template("scan.html")

# 🚪 تسجيل خروج
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ▶️ تشغيل
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
