import consul
import mysql.connector
import logging

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Get credentials from Consul
c = consul.Consul(host="10.68.69.136", token="30126abf-691c-4d1a-b7da-e4c4b578dd4a")
DB_USER = c.kv.get("flex/shared/flex-enterprise/mysql/username")[1]['Value'].decode('utf-8')
DB_PASSWORD = c.kv.get("flex/shared/flex-enterprise/mysql/password")[1]['Value'].decode('utf-8')
DB_NAME = c.kv.get("flex/shared/flex-enterprise/mysql/database")[1]['Value'].decode('utf-8')
DB_HOST = c.kv.get("flex/shared/mysql/host")[1]['Value'].decode('utf-8')
DB_PORT = int(c.kv.get("flex/shared/mysql/port")[1]['Value'].decode('utf-8'))

print(f"Connecting to database with: {DB_USER}, {DB_HOST}, {DB_NAME}, {DB_PORT}, {DB_PASSWORD}")

try:
    # Connect directly to the MySQL/MariaDB database
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=10
    )

    # Get a cursor object
    cursor = conn.cursor()

    # Execute a sample query
    cursor.execute("SHOW TABLES;")
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the connection
    cursor.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
