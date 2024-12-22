import sqlite3

def database_query(input, password):
    # Create sample table
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'password123')")

    # Normal queries
    # query = f"SELECT * FROM users WHERE username = '{input}' and password = '{password}'"
    # cursor.execute(query)

# --------------- IMPLEMENT SQL Injection prevention - sanitisation  ---------------   
    query = "SELECT * FROM users WHERE username = ? and password = ?"
    cursor.execute(query, (input, password))
# --------------- IMPLEMENT SQL Injection prevention - sanitisation  ---------------    

    print(f"Executing query: {query}")

    result = cursor.fetchall()
    conn.close()

    return result

# Attack using SQL Injection
print(database_query("admin", "password123"))
print(database_query("admin' --", "test"))
