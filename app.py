from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# FORMS
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, SelectField, PasswordField, TextAreaField, FileField, MultipleFileField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError, SelectMultipleField, widgets
import email_validator

class TargetForm(FlaskForm):
    url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    response = requests.get(url)
    data = response.json()
    d=[]
    for i in data:
        d.append((i['Object'],i['Object']))

    object = RadioField('Which object do you want to target?', choices=d, validators=[DataRequired()])
    apikey=StringField('Your API key', validators=[DataRequired()])
    listid=StringField('List ID', validators=[DataRequired()])
    submit = SubmitField('SAVE')

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
    url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    response = requests.get(url)
    data = response.json()
    arranged_data = arrange_data(data)
    form = TargetForm()
    if form.validate_on_submit():
        print('Form submitted')
        print(form.esp.data)
        print(form.apikey.data)
        print(form.listid.data)
    return render_template('index.html', form=form, arranged_data=arranged_data)

@app.route('/send/', methods=['POST'])
def send():
    return request.form

@app.route('/team/')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)

