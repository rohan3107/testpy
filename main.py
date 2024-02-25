from flask import Flask, request, render_template_string, escape
from os import path
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/view-file')
def view_file():
    file_name = request.args.get('file')  # User-supplied input without proper sanitization
    if file_name:
        file_name = path.join('safe_directory', path.basename(file_name))  # Sanitize file path
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            content = escape(content)  # Escape HTML content
            return render_template_string('<h1>File Content</h1><pre>{{ content }}</pre>', content=content)
    except Exception as e:
        return render_template_string('<h1>Error</h1><p>Could not read file.</p>')

@app.route('/search')
def search():
    query = request.args.get('query')  # User-supplied input without proper escaping
    query = escape(query)  # Escape HTML content
    return render_template_string('<h1>Search Results</h1><p>No results found for: {{ query }}</p>', query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Use parameterized queries to prevent SQL injection
        query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        
        # Create a database session and execute the parameterized query
        # For demonstration only. In a real scenario, you would use an actual database connection.
        Session = sessionmaker()
        session = Session()
        result = session.execute(query, {'username': username, 'password': password})
        
        username = escape(username)  # Escape HTML content
        return render_template_string('<h1>Login Successful</h1><p>Welcome back, {{ username }}!</p>', username=username)
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
    app.run(debug=False)  # Disable debug mode
