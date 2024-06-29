from flask import Flask, render_template
import requests

app = Flask(__name__)

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
    return render_template('index.html', arranged_data=arranged_data)

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)

