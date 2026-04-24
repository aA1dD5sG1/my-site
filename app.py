from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"  # غيرها لاحقاً

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# الصفحة الرئيسية
@app.route("/")
def home():
    if "user" in session:
        return f"مرحباً {session['user']} 👋"
    return redirect("/login")

# تسجيل
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, hashed))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "المستخدم موجود مسبقاً ❌"

    return render_template("register.html")

# تسجيل دخول
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[2], password):
            session["user"] = user
            return redirect("/")
        else:
            return "بيانات خاطئة ❌"

    return render_template("login.html")

# تسجيل خروج
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
