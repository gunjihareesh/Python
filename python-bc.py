
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import boto3
import json

app = Flask(__name__)
CORS(app)

# ===============================
# AWS Secrets Manager Configuration
# ===============================
SECRET_NAME = "rds!db-66f01397-5836-43af-917e-5738a85b70a0"     # Your Secret Name
REGION_NAME = "us-east-1"

# ===============================
# Get Password from Secrets Manager
# ===============================
def get_db_password():
    session = boto3.session.Session()

    client = session.client(
        service_name="secretsmanager",
        region_name=REGION_NAME
    )

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    secret = json.loads(response["SecretString"])

    return secret["password"]


# ===============================
# Database Connection
# ===============================
def get_db_connection():

    password = get_db_password()

    return mysql.connector.connect(
        host="database-1.cppnllsooubv.us-east-1.rds.amazonaws.com",
        user="admin",
        password=password,
        database="dev",
        port=3306
    )


# ===============================
# Home Route
# ===============================
@app.route("/")
def index():
    return "Backend API Running"


# ===============================
# Get All Users
# ===============================
@app.route("/users", methods=["GET"])
def get_users():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# Get User By ID
# ===============================
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM users WHERE id=%s",
            (user_id,)
        )

        user = cursor.fetchone()

        if user:
            return jsonify(user)

        return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# Add User
# ===============================
@app.route("/users/add", methods=["POST"])
def add_user():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            return jsonify({"error": "User already exists"}), 409

        cursor.execute(
            "INSERT INTO users(name,email) VALUES(%s,%s)",
            (name, email)
        )

        conn.commit()

        return jsonify({"message": "User added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# Update User
# ===============================
@app.route("/users/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT id FROM users WHERE id=%s",
            (user_id,)
        )

        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute(
            """
            UPDATE users
            SET name=%s,
                email=%s
            WHERE id=%s
            """,
            (name, email, user_id)
        )

        conn.commit()

        return jsonify({"message": "User updated successfully"})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# Delete User
# ===============================
@app.route("/users/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT id FROM users WHERE id=%s",
            (user_id,)
        )

        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute(
            "DELETE FROM users WHERE id=%s",
            (user_id,)
        )

        conn.commit()

        return jsonify({"message": "User deleted successfully"})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# Run Flask App
# ===============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
