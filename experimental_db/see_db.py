import sqlite3

# Connect to the SQLite database (replace 'your_database.db' with your actual database file)
conn = sqlite3.connect('experimental_db\sample_database.db')
cursor = conn.cursor()

# Execute a simple query (e.g., select all rows from the 'student' table)
# cursor.execute('''SELECT * FROM student WHERE issue_priority = "p0" ;''')

query = "PRAGMA table_info({table_name})".format(table_name='student')
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Print the rows
i=0
# for row in rows:
#     print(row)
#     i+=1
#     if i==10:
#         break

column_names = [column[1] for column in rows]

# Print column names
print(column_names)
# Close the connection
conn.close()