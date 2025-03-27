import os
import subprocess
import sys

# Check if virtual environment is activated
in_venv = sys.prefix != sys.base_prefix

if not in_venv:
    print("Virtual environment not activated.")
    print("Please activate the virtual environment with:")
    print("  On Windows: .\\venv\\Scripts\\activate")
    print("  On Unix/Linux: source venv/bin/activate")
    sys.exit(1)

# Check if .env file exists
if not os.path.exists('.env'):
    print("Error: .env file not found.")
    print("Please create a .env file with the required variables.")
    sys.exit(1)

try:
    # Install required packages
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Setup database
    print("Setting up database...")
    subprocess.run([sys.executable, "setup_db.py"], check=True)
    
    # Run Flask application
    print("Starting Flask application...")
    os.chdir("Frontend")
    subprocess.run([sys.executable, "app.py"], check=True)
    
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1) 