from flask import Flask, request, render_template_string, escape
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query using parameterized statements
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Using parameterized query to prevent SQL injection
    result = cursor.fetchone()
    if result:
        return 'Login Successful!'
    else:
        return 'Login Failed!'

@app.route('/comment', methods=['GET'])
def comment():
    user_input = request.args.get('text')
    # Escaping user input to prevent template injection
    safe_user_input = escape(user_input)
    return render_template_string(f'User comment: {safe_user_input}')  # Rendering escaped user input

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Validate or sanitize the host parameter to prevent command injection
    safe_host = re.sub(r'[^a-zA-Z0-9.-]', '', host)
    command = f"ping -c 1 {safe_host}"  # Using sanitized host parameter
    result = os.popen(command).read()  # Executing the command with sanitized input
    return f'<pre>{result}</pre>'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Use secure_filename to prevent path injection attacks
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Saving the file with a secure filename
    return f'File uploaded successfully to {file_path}.'

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
