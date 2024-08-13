# app.py
from flask import Flask
from config import Config
from utils.extensions import db, bcrypt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

from routes import auth, llm, user

app.register_blueprint(auth.bp)
app.register_blueprint(llm.bp)
app.register_blueprint(user.bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
