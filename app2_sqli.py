from flask import Flask, request
import sqlite3

app = Flask(__name__)

# 1. Initialize the mock e-commerce database
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    cursor.execute('DELETE FROM users') # Reset table on restart
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'SuperSecretAdminPassword123')")
    conn.commit()
    conn.close()

init_db()

# 2. Host a simple login form
@app.route('/')
def index():
    return '''
    <h2>E-Commerce Login</h2>
    <form method="POST" action="/login">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    '''

# 3. SECURE Login Handler (Using Parameterized Queries)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # SECURE: Parameterized queries use '?' as placeholders, neutralizing SQL payloads
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        return f"<h3>Login Successful!</h3><p>Welcome, {user[0]}.</p>"
    else:
        return "<h3>Login Failed.</h3><p>Invalid credentials.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    #http://127.0.0.1:5000
    #username: admin' --