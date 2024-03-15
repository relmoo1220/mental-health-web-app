import sqlite3

conn = sqlite3.connect("database.db")
print("Connected to database successfully")

conn.execute("CREATE TABLE answers (id INTEGER PRIMARY KEY AUTOINCREMENT, question1 TEXT, question2 TEXT, question3 TEXT, question4 TEXT)")
print("Table created successfully")

conn.close()