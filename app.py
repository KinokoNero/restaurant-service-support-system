from flask import Flask, render_template
from authentication import auth_routes, login_manager
from database import db_routes, menu_collection
from session import session_routes
from flask_login import login_required

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'c9383efdbb41c23072b029ecc4789e36'
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(db_routes, url_prefix='/db')
app.register_blueprint(session_routes, url_prefix='/session')
login_manager.init_app(app)

@app.route('/menu')
#@login_required
def menu():
    items = menu_collection.find()
    return render_template('menu.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)