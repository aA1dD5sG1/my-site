from flask import Flask, request, redirect
import os
import sys

app = Flask(__name__)

# تسجيل كل الطلبات
@app.before_request
def log_request_info():
    print("\n====== NEW REQUEST ======", flush=True)
    print("IP:", request.remote_addr, flush=True)
    print("Method:", request.method, flush=True)
    print("URL:", request.url, flush=True)
    print("User-Agent:", request.headers.get('User-Agent'), flush=True)
    
    if request.method == "POST":
        print("POST DATA:", request.form, flush=True)
    else:
        print("GET PARAMS:", request.args, flush=True)

# الصفحة الرئيسية
@app.route('/')
def home():
    return "<h1>Home Page</h1>"

# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print("====== LOGIN ATTEMPT ======", flush=True)
        print("Username:", username, flush=True)
        print("Password:", password, flush=True)
        sys.stdout.flush()

        if username == "admin" and password == "1234":
            return redirect("/dashboard")
        else:
            return "Login Failed"

    return '''
    <form method="POST" action="/login">
        <input name="username" placeholder="Username" required><br>
        <input name="password" type="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    '''

# لوحة التحكم
@app.route('/dashboard')
def dashboard():
    return "<h1>Dashboard</h1>"

# تسجيل الخروج
@app.route('/logout')
def logout():
    return redirect('/login')


# تشغيل مناسب لـ Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
