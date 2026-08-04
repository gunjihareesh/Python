import mysql.connector

# Connect to your existing database
conn = mysql.connector.connect(
    host="database-1.c91d775knpjs.us-east-1.rds.amazonaws.com",        # or your RDS endpoint
    user="admin",             # replace with your username
    password="test123cg", # replace with your password
    database="dept"        # your existing database
)

cursor = conn.cursor()

# Insert a single new record
insert_query = """
INSERT INTO Employees (FirstName, LastName, Department, Salary)
VALUES (%s, %s, %s, %s)
"""
new_employee = ("Anita", "Kumar", "Sales", 58000.00)
cursor.execute(insert_query, new_employee)
conn.commit()
print("1 record inserted.")

# Insert multiple new records at once
records = [
    ("Raj", "Patel", "Engineering", 67000.00),
    ("Meena", "Sharma", "Finance", 72000.00),
    ("Arjun", "Reddy", "HR", 56000.00)
]

cursor.executemany(insert_query, records)
conn.commit()
print(cursor.rowcount, "new records inserted.")

# Optional: Verify by selecting all rows
cursor.execute("SELECT * FROM Employees")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
