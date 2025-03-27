import os
import time
import logging
import mysql.connector
from dotenv import load_dotenv
import sys
import datetime
import shutil
from pathlib import Path

# Import telescope control functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telescope_control import capture_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("telescope_scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TelescopeScheduler")

# Load environment variables
load_dotenv("../.env")

# Database connection parameters
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'webportal'),
    'password': os.environ.get('MYSQL_PASSWORD', 'SEDSCelestia123'),
    'database': os.environ.get('DB_NAME', 'telescope')
}

# Image storage configuration
IMAGE_DIR = os.environ.get('IMAGE_DIR', 'images')
Path(IMAGE_DIR).mkdir(exist_ok=True)

def get_db_connection():
    """Establish and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        return None

def get_pending_requests():
    """Get all requests with 'not captured' status"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, exposure_time, object, email 
            FROM webportal 
            WHERE status = 'not captured'
            ORDER BY request_date, request_time
        """)
        requests = cursor.fetchall()
        cursor.close()
        conn.close()
        return requests
    except mysql.connector.Error as err:
        logger.error(f"Error fetching pending requests: {err}")
        if conn.is_connected():
            conn.close()
        return []

def update_request_status(request_id, status, image_path):
    """Update the status and image path for a specific request"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE webportal 
            SET status = %s, image_path = %s 
            WHERE id = %s
        """, (status, image_path, request_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        logger.error(f"Error updating request status: {err}")
        if conn.is_connected():
            conn.rollback()
            conn.close()
        return False

def process_request(request):
    """Process a single telescope observation request"""
    request_id = request['id']
    object_name = request['object']
    exposure_time_str = request['exposure_time']
    
    # Convert exposure_time from string to seconds if needed
    try:
        if isinstance(exposure_time_str, str):
            h, m, s = exposure_time_str.split(':')
            exposure_seconds = int(h) * 3600 + int(m) * 60 + int(s)
        else:
            # If it's already a datetime.time object
            exposure_seconds = exposure_time_str.hour * 3600 + exposure_time_str.minute * 60 + exposure_time_str.second
    except Exception as e:
        logger.error(f"Error processing exposure time '{exposure_time_str}': {e}")
        exposure_seconds = 10  # Default exposure time
    
    logger.info(f"Processing request {request_id} - Object: {object_name}, Exposure: {exposure_seconds}s")
    
    try:
        # 1. Point telescope at the object (this would call your existing telescope control code)
        logger.info(f"Pointing telescope at {object_name}")
        # TODO: Add code to point telescope using existing scripts
        
        # 2. Capture image (using your existing capture function)
        logger.info(f"Capturing image with {exposure_seconds}s exposure")
        image_path = capture_image(object_name, exposure_seconds)
        
        # If capture_image() is not implemented yet, create a mock implementation
        if image_path is None:
            # Create a timestamp-based filename for the image
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{object_name.replace(' ', '_')}.jpg"
            image_path = os.path.join(IMAGE_DIR, filename)
            
            # For testing: copy a placeholder image or create an empty file
            logger.info(f"Creating placeholder image at {image_path}")
            with open(image_path, 'w') as f:
                f.write("Placeholder image file")
        
        # 3. Update database with status = 'captured' and image_path
        if update_request_status(request_id, 'captured', image_path):
            logger.info(f"Request {request_id} updated: Status = captured, Image = {image_path}")
            return True
        else:
            logger.error(f"Failed to update status for request {request_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}")
        return False

def main_loop():
    """Main processing loop that runs continuously"""
    logger.info("Starting telescope scheduler")
    
    while True:
        try:
            # Check for pending requests
            requests = get_pending_requests()
            
            if requests:
                logger.info(f"Found {len(requests)} pending requests")
                
                # Process each request
                for request in requests:
                    process_request(request)
                    # Sleep briefly between requests to prevent system overload
                    time.sleep(2)
            else:
                logger.info("No pending requests found")
            
            # Sleep before checking again
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Error in main processing loop: {e}")
            time.sleep(60)  # Sleep and retry

if __name__ == "__main__":
    main_loop()