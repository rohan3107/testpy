from flask import Flask, request, render_template_string, escape
import re

app = Flask(__name__)

@app.route('/view-file')
def view_file():
    file_name = request.args.get('file')
    file_name = re.sub('[^A-Za-z0-9.]+', '', file_name)
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return render_template_string('<h1>File Content</h1><pre>' + content + '</pre>')
    except Exception as e:
        return render_template_string('<h1>Error</h1><p>Could not read file.</p>')

@app.route('/search')
def search():
    query = request.args.get('query')
    query = escape(query)
    return render_template_string('<h1>Search Results</h1><p>No results found for: ' + query + '</p>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        parameters = [username, password]
        print('Executing query: ' + query)
        print('With parameters: ' + str(parameters))
        return render_template_string('<h1>Login Successful</h1><p>Welcome back, ' + username + '!</p>')
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
    app.run(debug=True)