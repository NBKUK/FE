from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# In-memory mock database (for simplicity)
users_db = {'admin': generate_password_hash('password123')}
bank_details_db = {}
crypto_payouts = {'USDC': 0, 'ETH': 0}

# Home route
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db and check_password_hash(users_db[username], password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Invalid credentials")
    return render_template('index.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

# Payout route (Crypto)
@app.route('/payout', methods=['POST', 'GET'])
def payout():
    if 'logged_in' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        crypto_type = request.form['crypto_type']
        amount = request.form['amount']

        if crypto_type in crypto_payouts:
            crypto_payouts[crypto_type] += float(amount)
            return redirect(url_for('dashboard'))

    return render_template('payout.html', crypto_payouts=crypto_payouts)

# Bank info route
@app.route('/bank-info', methods=['POST', 'GET'])
def bank_info():
    if 'logged_in' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        if bank_name and account_number:
            bank_details_db['bank_name'] = bank_name
            bank_details_db['account_number'] = account_number
            return redirect(url_for('dashboard'))

    return render_template('bank_info.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
