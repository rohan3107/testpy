from flask import Flask, request, escape
import sqlite3
import os
import shlex

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))  # Parameterized query to prevent SQL injection
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    safe_user_input = escape(user_input)  # Escaping user input to prevent XSS
    return f'User comment: {safe_user_input}'

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    safe_host = shlex.quote(host)  # Sanitizing the host parameter to prevent OS command injection
    command = f"ping -c 1 {safe_host}"
    result = os.popen(command).read()
    return f'<pre>{escape(result)}</pre>'  # Escaping the result to prevent XSS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join('uploads', escape(filename))  # Escaping the filename to prevent XSS
    file.save(file_path)
    return f'File uploaded successfully to {escape(file_path)}.'  # Escaping the file path to prevent XSS

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
