from flask import Flask, render_template
from pymongo import MongoClient
from authorization import auth_routes, login_manager

app = Flask(__name__)
app.secret_key = 'c9383efdbb41c23072b029ecc4789e36'
app.register_blueprint(auth_routes, url_prefix='/admin')
login_manager.init_app(app)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]

@app.route('/')
def main_page():
    menu = db["menu"]
    items = menu.find()
    return render_template('main-page.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)