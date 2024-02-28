from flask import Flask, request, render_template_string, escape
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your actual secret key

@app.route('/view-file')
def view_file():
    file_name = request.args.get('file')  # User-supplied input without proper sanitization
    if not os.path.basename(file_name) == file_name or '..' in file_name:
        return render_template_string('<h1>Error</h1><p>Invalid file name.</p>')
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return render_template_string('<h1>File Content</h1><pre>{{ content }}</pre>', content=content)
    except Exception as e:
        return render_template_string('<h1>Error</h1><p>Could not read file.</p>')

@app.route('/search')
def search():
    query = request.args.get('query')  # User-supplied input without proper escaping
    return render_template_string('<h1>Search Results</h1><p>No results found for: {{ query }}</p>', query=escape(query))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # This is a mock SQL query to demonstrate vulnerability. In a real scenario, this would be executed against a database.
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        
        # Vulnerable SQL query execution (hypothetical)
        # For demonstration only. Do not execute SQL queries this way.
        print("Executing query: " + query)
        
        return render_template_string('<h1>Login Successful</h1><p>Welcome back, {{ username }}</p>', username=escape(username))
    else:
        return '''
            <h1>Login</h1>
            <form method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            '''

if __name__ == '__main__':
    app.run(debug=False)
