from flask import Flask, request, render_template_string, escape
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Secure SQL query using parameterized statements
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
    # Escape user input to prevent XSS
    safe_user_input = escape(user_input)
    return render_template_string(f'User comment: {safe_user_input}')  # Render escaped user input

@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Validate and sanitize the host parameter to prevent OS command injection
    safe_host = re.sub(r'[^a-zA-Z0-9.-]', '', host)
    command = f"ping -c 1 {safe_host}"  # Use the sanitized host parameter
    result = os.popen(command).read()  # Executing the command with sanitized input
    return f'<pre>{escape(result)}</pre>'  # Escape the result to prevent XSS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)  # Use secure_filename to sanitize the file name
    file_path = os.path.join('uploads', filename)
    if filename == '':
        return 'No selected file.'
    if file and allowed_file(filename):
        file.save(file_path)  # Save the file after checking its content
        return f'File uploaded successfully to {escape(file_path)}.'
    else:
        return 'Invalid file type.'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
