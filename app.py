from flask import Flask
from config import Config
from models import db
from models.user import User
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to the Finance Tracker!"

if __name__ == "__main__":
    app.run(debug=True)