from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
import qrcode
import io

app = Flask(__name__)
app.secret_key = 'superkey'

# Temporary user storage (in-memory)
users = {}

@app.route('/')
def home():
    return render_template('home.html')

# ✅ LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]['password'] == password:
            session['user'] = users[email]['first_name']
            flash("Login successful!")
            return redirect(url_for('generate_qr'))
        else:
            flash("Invalid email or password! Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

# ✅ REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        password = request.form.get('password')

        if email in users:
            flash("Email already registered! Please login.")
            return redirect(url_for('login'))

        users[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'gender': gender,
            'password': password
        }

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')

# ✅ QR GENERATION (same as before)
@app.route('/generate', methods=['GET', 'POST'])
def generate_qr():
    if 'user' not in session:
        flash("Please login first!")
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form.get('data')
        if not data:
            flash("Please enter some data to generate a QR code.")
            return redirect(url_for('generate_qr'))

        img = qrcode.make(data)
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png')

    return render_template('generate.html')

# ✅ LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
