from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# Step 1: Connect to MySQL server (adjust host, user, password)
conn = mysql.connector.connect(
    host="database-1.c91d775knpjs.us-east-1.rds.amazonaws.com",       # or your RDS endpoint
    user="admin",            # replace with your username
    password="test123cg" # replace with your password
)

cursor = conn.cursor()

# Step 2: Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS dept")
cursor.execute("USE dept")

# Step 3: Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Department VARCHAR(50),
    Salary DECIMAL(10,2)
)
""")

# Step 4: Insert records
insert_query = """
INSERT INTO Employees (FirstName, LastName, Department, Salary)
VALUES (%s, %s, %s, %s)
"""
records = [
    ("John", "Doe", "IT", 60000.00),
    ("Jane", "Smith", "HR", 55000.00),
    ("Robert", "Brown", "Finance", 70000.00),
    ("Emily", "Davis", "Marketing", 50000.00)
]

cursor.executemany(insert_query, records)
conn.commit()

print(cursor.rowcount, "records inserted.")

# Step 5: Verify
cursor.execute("SELECT * FROM Employees")
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()

# =========================
# Health Check
# =========================
@app.route('/')
def index():
    return "RDS Master API running"

# =========================
# Entry Point
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
