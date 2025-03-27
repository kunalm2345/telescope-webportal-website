import mysql.connector
import os
import dotenv

# Load environment variables
dotenv.load_dotenv("../.env")

# Connect to MySQL using environment variables
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("MYSQL_USER", "webportal"),
    passwd=os.environ.get("MYSQL_PASSWORD", "SEDSCelestia123"),
    database=os.environ.get("DB_NAME", "telescope")
)
cur = db.cursor()

cur.execute("")