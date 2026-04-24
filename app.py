from flask import Flask, request, render_template, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "secret123"

# 📦 إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 🏠 الصفحة الرئيسية
@app.route("/")
def home():
    return redirect("/login")

# 🔐 تسجيل دخول
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("db.db")
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (user,))
        result = cur.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "❌ خطأ في تسجيل الدخول"

    return render_template("login.html")

# 📝 تسجيل مستخدم
@app.route("/register", methods=["POST"])
def register():
    user = request.form.get("username")
    password = request.form.get("password")

    hashed = generate_password_hash(password)

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed))
    conn.commit()
    conn.close()

    return redirect("/login")

# 📊 لوحة التحكم
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

# 🚪 تسجيل خروج
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# 🔥 السطر المهم (للـ Render والسيرفرات)
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))