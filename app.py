from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

# تسجيل كل الطلبات (قبل تنفيذ أي route)
@app.before_request
def log_request_info():
    print("\n====== NEW REQUEST ======")
    print("IP:", request.remote_addr)
    print("Method:", request.method)
    print("URL:", request.url)
    print("User-Agent:", request.headers.get('User-Agent'))
    
    if request.method == "POST":
        print("POST DATA:", request.form)
    else:
        print("GET PARAMS:", request.args)

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

        print("LOGIN ATTEMPT:")
        print("Username:", username)
        print("Password:", password)

        # مثال بسيط
        if username == "admin" and password == "1234":
            return redirect("/dashboard")
        else:
            return "Login Failed"

    return '''
    <form method="POST">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
