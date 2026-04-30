import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2

# Load .env file
load_dotenv()

app = Flask(__name__)

# ✅ DB connection function
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432,
        sslmode="require"
    )

# ✅ Home route
@app.route("/")
def home():
    return jsonify({"message": "Flask API running 🚀"})

# ✅ Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ✅ DB test
@app.route("/db-test")
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT version();")
        version = cur.fetchone()

        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "db_version": version[0]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ✅ Get users
@app.route("/users")
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users;")
        rows = cur.fetchall()

        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1],
                "email": row[2]
            })

        cur.close()
        conn.close()

        return jsonify(users)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ✅ Create user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (data["name"], data["email"])
        )

        new_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "User created",
            "id": new_id
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))  # local = 5000, Azure = 80
    app.run(host="0.0.0.0", port=port)