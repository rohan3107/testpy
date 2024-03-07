from flask import Flask, request, render_template_string, escape
import sqlite3
import os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query using parameterized statements
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    connection = sqlite3.connect('application.db')
    cursor = connection.cursor()
    cursor.execute(query, (username, password))  # Using parameters to prevent SQL injection
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
    # Validate or sanitize the host parameter to prevent OS command injection
    safe_host = re.sub(r'[^a-zA-Z0-9.:-]', '', host)
    command = f"ping -c 1 {safe_host}"  # Using a sanitized host parameter
    result = os.popen(command).read()  # Executing the command
    return f'<pre>{escape(result)}</pre>'  # Escaping the result to prevent XSS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    # Ensure the filename is safe to use
    safe_filename = secure_filename(filename)
    file_path = os.path.join('uploads', safe_filename)
    file.save(file_path)  # Saving the file with a safe filename
    # Escaping the file path to prevent XSS
    return f'File uploaded successfully to {escape(file_path)}.'

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
