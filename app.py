from flask import Flask, render_template
from database import db_routes, menu_collection
from authentication import auth_routes, login_manager
from flask_login import login_required#LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'c9383efdbb41c23072b029ecc4789e36'
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(db_routes, url_prefix='/db')
login_manager.init_app(app)

@app.route('/')
#@login_required
def main_page():
    items = menu_collection.find()
    return render_template('main_page.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)