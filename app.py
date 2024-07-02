from flask import Flask, render_template
import requests

app = Flask(__name__)

# FORMS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField, FileField, MultipleFileField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError, SelectMultipleField, widgets
import email_validator

class TargetForm(FlaskForm):
    esp = SelectField('Which app do you send your newsletter?', choices=[('ml','MailerLite'), ('ck', 'Convertkit'), ('gh', 'Ghost'), ('rv', 'Revue'), ('eo', 'EmailOctopus'), ('sf', 'SendFox'), ('ac', 'ActiveCampaign'), ('br', 'Brevo (Sendinblue)'),], validators=[DataRequired()])
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
    form = TargetForm()
    if form.validate_on_submit():
        print('Form submitted')
        print(form.esp.data)
        print(form.apikey.data)
        print(form.listid.data)
    url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    response = requests.get(url)
    data = response.json()
    arranged_data = arrange_data(data)
    return render_template('index.html', form=form, arranged_data=arranged_data)

@app.route('/team/')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)

