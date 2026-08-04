import mysql.connector

# Connect to MySQL Server
conn = mysql.connector.connect(
    host="database-1.cslu0ymw212o.us-east-1.rds.amazonaws.com",
    user="admin",
    password="test123cg"
)

cursor = conn.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS users")
print("Database created successfully")

# Select Database
cursor.execute("USE users")

# Insert Records
sql = """
INSERT INTO employees (name, email, salary)
VALUES (%s, %s, %s)
"""

employees = [
    ("Hareesh123", "hareesh123@example.com", 50000)
]

cursor.executemany(sql, employees)

conn.commit()

print(f"{cursor.rowcount} records inserted successfully")

# Display Records
cursor.execute("SELECT * FROM employees")

rows = cursor.fetchall()

print("\nEmployee Records:")
for row in rows:
    print(row)

# Close Connection
cursor.close()
conn.close()
