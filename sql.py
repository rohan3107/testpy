import sqlite3

def safe_query(database_path, username, password):
    # Establish a connection to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    
    sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result:
            return "Login successful."
        else:
            return "Login failed."
    except sqlite3.Error as error:
        return f"An error occurred: {error}"
    finally:
        connection.close()
