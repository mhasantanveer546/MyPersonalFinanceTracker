from flask import Flask
from config import Config
from models import db
from models.user import User
from routes.auth_routes import auth_bp
from flask_login import LoginManager
from models.transaction import Transaction
from routes.transaction_routes import transaction_bp
from models.budget import Budget
from routes.budget_routes import budget_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(dashboard_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to the Finance Tracker!"

if __name__ == "__main__":
    app.run(debug=True)