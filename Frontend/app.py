# from flask import Flask, render_template, request, jsonify
# import requests
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Email
# from datetime import datetime, timedelta, timezone

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'

# # Configuration for MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kali@localhost/telescope'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define the form
# class DataForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     exposure_time = StringField('Exposure Time', validators=[DataRequired()])
#     obj = StringField('Object', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Submit')

# class Data(db.Model):
#     __tablename__ = 'webportal'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)
#     exposure_time = db.Column(db.Time)
#     object = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     request_date = db.Column(db.Date)
#     request_time = db.Column(db.Time)
#     status = db.Column(db.Enum('not captured', 'captured', 'mailed'), default='not captured', nullable=False)
#     image_path = db.Column(db.String(255), default='/image')

#     def __repr__(self):
#         return f'<Data {self.name} - {self.obj}>'

# def arrange_data(data):
#     result = {}
#     for item in data:
#         category = item.get('Category')
#         obj = item.get('Object')
#         image_link = item.get('Image link')

#         if category not in result:
#             result[category] = {}
        
#         result[category][obj] = image_link
    
#     return result

# @app.route('/')
# def home():
#     url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
#     response = requests.get(url)
#     data = response.json()
#     arranged_data = arrange_data(data)
#     return render_template('index.html', arranged_data=arranged_data)

# @app.route('/send/', methods=['POST'])
# def send():
#     name = request.form.get('name')
#     exposure_time = request.form.get('exposure')
#     object = request.form.get('object')
#     email = request.form.get('email')
#     ist_offset = timedelta(hours=5, minutes=30)
#     ist_timezone = timezone(ist_offset)
#     current_datetime = datetime.now(ist_timezone)

#     new_data = Data(
#         name=name, 
#         exposure_time=exposure_time, 
#         object=object, 
#         email=email, 
#         request_date=current_datetime.date(), 
#         request_time=current_datetime.time(),
#         status=False  # Set default value for is_mail_sent to False
#     )
#     db.session.add(new_data)
#     db.session.commit()

#     return jsonify({'message': 'Data added successfully!'})

# @app.route('/team/')
# def team():
#     return render_template('team.html')

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta, timezone
import dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv("../.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')

# Configuration for MySQL using environment variables
connection_string = f'mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"Connecting to database at {os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}")

db = SQLAlchemy(app)

# Define the form
class DataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    exposure_time = StringField('Exposure Time', validators=[DataRequired()])
    object = StringField('Object', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class Data(db.Model):
    __tablename__ = 'webportal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    exposure_time = db.Column(db.Time)
    object = db.Column(db.String(255))
    email = db.Column(db.String(255))
    request_date = db.Column(db.Date)
    request_time = db.Column(db.Time)
    status = db.Column(db.Enum('not captured', 'captured', 'mailed'), default='not captured', nullable=False)
    image_path = db.Column(db.String(255), default='/image')

    def __repr__(self):
        return f'<Data {self.name} - {self.obj}>'

def arrange_data(data):
    result = {}
    for item in data:
        category = item.get('Category')
        obj = item.get('Object')
        image_link = item.get('Image link')

        if category not in result:
            result[category] = {}
        
        result[category][obj] = image_link
    
    return result

@app.route('/')
def home():
    # url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    # response = requests.get(url)
    # data = response.json()

    data = [{"Object":"Moon","Category":"Solar System","Image link":"https://c02.purpledshub.com/uploads/sites/48/2019/04/The-Moon-fafa62f.jpg?w=1029&webp=1"},{"Object":"Sun","Category":"Nebulae","Image link":"https://www.quantamagazine.org/wp-content/uploads/2018/07/SolarFull_SeanDoran_2880FullwidthLede.jpg"},{"Object":"Saturn","Category":"Solar System","Image link":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg"},{"Object":"Saturn4","Category":"Solar System","Image link":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg"},{"Object":"Saturn3","Category":"Solar System","Image link":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg"},{"Object":"Saturn2","Category":"Solar System","Image link":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg"}]
    
    arranged_data = arrange_data(data)
    return render_template('index.html', arranged_data=arranged_data)

@app.route('/send/', methods=['POST'])
def send():
    try:
        name = request.form.get('name')
        exposure_time = request.form.get('exposure')
        object_name = request.form.get('object')
        email = request.form.get('email')
        
        # Validate required fields
        if not all([name, exposure_time, object_name, email]):
            return jsonify({'error': 'All fields are required'}), 400
            
        # Verify email domain (optional)
        if not email.endswith('bits-pilani.ac.in'):
            return jsonify({'error': 'Please use a BITS email address'}), 400
            
        ist_offset = timedelta(hours=5, minutes=30)
        ist_timezone = timezone(ist_offset)
        current_datetime = datetime.now(ist_timezone)

        # Convert exposure time to TIME format
        try:
            exposure_seconds = int(exposure_time)
            hours = exposure_seconds // 3600
            minutes = (exposure_seconds % 3600) // 60
            seconds = exposure_seconds % 60
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except ValueError:
            formatted_time = exposure_time

        new_data = Data(
            name=name, 
            exposure_time=formatted_time, 
            object=object_name, 
            email=email, 
            request_date=current_datetime.date(), 
            request_time=current_datetime.time(),
            status='not captured',
            image_path='/image'
        )
        
        db.session.add(new_data)
        db.session.commit()
        
        return jsonify({
            'message': 'Data added successfully!',
            'id': new_data.id
        }), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving data: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/team/')
def team():
    return render_template('team.html')

@app.route('/photos/')
def photos():
    # Get last 10 requests that have images (excluding default /image path)
    photos = Data.query.filter(Data.image_path != '/image')\
                      .order_by(Data.id.desc())\
                      .limit(10)\
                      .all()
    return render_template('photos.html', photos=photos)

@app.route('/done/<int:id>')
def done(id):
    data = Data.query.get_or_404(id)
    if data.image_path and data.image_path != '/image':
        return render_template('done.html', image_url=data.image_path)
    return render_template('done.html', message="Your image will be ready in 1-2 days. Please check your email.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
