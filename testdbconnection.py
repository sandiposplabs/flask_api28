import psycopg2

try:
    conn = psycopg2.connect(
        host="saludpsql.postgres.database.azure.com",
        database="postgres",
        user="saludpsladmin",   # ✅ FIXED
        password="Password@123",
        port=5432,
        sslmode="require"
    )

    print("✅ Connection successful!")

    cur = conn.cursor()
    cur.execute("SELECT version();")

    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)