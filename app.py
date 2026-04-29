from flask import Flask, render_template, request, redirect, session
import sqlite3
import secrets
import logging
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# =========================
# 🔥 إعداد logging
# =========================
logging.basicConfig(level=logging.INFO)

def log_request():
    logging.info(f"IP: {request.remote_addr}")
    logging.info(f"PATH: {request.path}")
    logging.info(f"METHOD: {request.method}")
    logging.info(f"FORM: {request.form}")

# =========================
# 🗄️ قاعدة البيانات
# =========================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        token TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 🏠 الصفحة الرئيسية
# =========================
@app.route("/")
def home():
    log_request()

    if "user" in session:
        return f"مرحباً {session['user']} 👋 <br><a href='/logout'>Logout</a>"
    return redirect("/login")

# =========================
# 📝 تسجيل
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    log_request()

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        logging.info(f"NEW REGISTER: {user}")

        hashed = generate_password_hash(password)

        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password, token) VALUES (?, ?, ?)",
                (user, hashed, None)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "المستخدم موجود مسبقاً ❌"

    return render_template("register.html")

# =========================
# 🔑 تسجيل دخول
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    log_request()

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        logging.info(f"LOGIN TRY: {user}")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[2], password):
            session["user"] = user
            logging.info(f"LOGIN SUCCESS: {user}")
            return redirect("/")
        else:
            logging.warning(f"LOGIN FAIL: {user}")
            return "بيانات خاطئة ❌"

    return render_template("login.html")

# =========================
# 🎫 توليد توكن
# =========================
@app.route("/generate-token")
def generate_token():
    log_request()

    if "user" not in session:
        return redirect("/login")

    token = secrets.token_urlsafe(32)

    logging.info(f"TOKEN GENERATED FOR: {session['user']}")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET token=? WHERE username=?", (token, session["user"]))
    conn.commit()
    conn.close()

    return f"""
    <h3>Token:</h3>
    <p>{token}</p>
    <a href="/token-login?token={token}">دخول بالتوكن</a>
    """

# =========================
# 🚀 تسجيل دخول بالتوكن
# =========================
@app.route("/token-login")
def token_login():
    log_request()

    token = request.args.get("token")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE token=?", (token,))
    result = c.fetchone()

    if result:
        session["user"] = result[0]

        logging.info(f"TOKEN LOGIN SUCCESS: {result[0]}")

        c.execute("UPDATE users SET token=NULL WHERE username=?", (result[0],))
        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()
    logging.warning("INVALID TOKEN USED")
    return "Token غير صالح ❌"

# =========================
# 🚪 تسجيل خروج
# =========================
@app.route("/logout")
def logout():
    log_request()

    user = session.get("user")
    session.pop("user", None)

    logging.info(f"LOGOUT: {user}")

    return redirect("/login")

# =========================
# ▶️ تشغيل
# =========================
if __name__ == "__main__":
    app.run(debug=True)
