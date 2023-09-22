from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]

@app.route('/')
def index():
    menu = db["menu"]
    data = list(menu.find())
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)