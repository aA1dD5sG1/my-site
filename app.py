from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template("index.html")

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        print("LOGIN:", username, password)

        return redirect(url_for('dashboard'))

    return render_template("login.html")

# لوحة التحكم
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# صفحة الفحص
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        url = request.form.get("url")

        results = []

        # فحص بسيط
        if not url.startswith("http"):
            results.append("❌ Invalid URL")
        else:
            results.append("⚠️ Missing X-Frame-Options")
            results.append("⚠️ Missing CSP")
            results.append("⚠️ Missing X-Content-Type-Options")
            results.append("ℹ️ Found 1 forms")

        return render_template("scan.html", results=results, target=url)

    return render_template("scan.html", results=None)
    

if __name__ == "__main__":
    app.run(debug=True)
