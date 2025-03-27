import mysql.connector
import os
import dotenv

# Load environment variables
dotenv.load_dotenv(".env")

def setup_database():
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "webportal"),
            passwd=os.environ.get("MYSQL_PASSWORD", "SEDSCelestia123")
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        db_name = os.environ.get("DB_NAME", "telescope")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS webportal (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            exposure_time TIME,
            object VARCHAR(255),
            email VARCHAR(255),
            request_date DATE,
            request_time TIME,
            status ENUM('not captured', 'captured', 'mailed') DEFAULT 'not captured',
            image_path VARCHAR(255) DEFAULT '/image'
        )
        ''')
        
        conn.commit()
        print(f"Database '{db_name}' and table 'webportal' setup completed successfully")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error setting up database: {err}")

if __name__ == "__main__":
    setup_database() 