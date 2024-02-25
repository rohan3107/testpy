from flask import Flask, request, render_template_string, escape
import sqlite3
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query construction using parameterized queries
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Execution of parameterized query
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    # Escaping user input to prevent XSS
    safe_user_input = escape(user_input)
    return render_template_string(f'User comment: {safe_user_input}')  # Rendering escaped user input

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Validate and sanitize the host parameter to prevent command injection
    if re.match(r'^[a-zA-Z0-9.:-]+$', host):
        command = f"ping -c 1 {host}"
        result = os.popen(command).read()
        return f'<pre>{escape(result)}</pre>'
    else:
        return 'Invalid host.'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Use secure_filename to prevent arbitrary file upload
    filename = secure_filename(file.filename)
    if filename != '':
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        return f'File uploaded successfully to {file_path}.'
    else:
        return 'Invalid file name.'

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
