# Telescope Web Portal

This is a web portal for the BITS Goa Observatory Telescope that allows students to schedule observations.

## Setup Instructions

1. Make sure you have Python 3.8+ installed
2. Set up a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Ensure MySQL is installed and running on your system
6. Configure your environment variables in the `.env` file:
   ```
   PORT=8090
   MYSQL_USER="your_mysql_username"
   MYSQL_PASSWORD="your_mysql_password"
   DB_NAME="telescope"
   DB_HOST="localhost"
   EMAIL=""
   PASSWORD=""
   ```
7. Run the setup script to create the database and tables:
   ```
   python setup_db.py
   ```
8. Run the application:
   ```
   python run.py
   ```
   
## Alternatively, use the one-step run script:

After setting up your `.env` file and activating your virtual environment, simply run:
```
python run.py
```

This will install dependencies, set up the database, and start the application.

## Usage

1. Navigate to `http://localhost:5000` in your web browser
2. Select a celestial object from the available options
3. Choose an exposure time
4. Enter your name and BITS email address
5. Submit the form to schedule your observation

The system will queue your request and send the image to your email once the observation is complete. 