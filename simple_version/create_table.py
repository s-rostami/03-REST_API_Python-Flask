import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)
print('table created')

cursor.execute("INSERT INTO items VALUES ('test',10.99)")
result = cursor.execute("SELECT * FROM items")
print(result.fetchone())

connection.commit()

connection.close()