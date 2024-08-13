from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from routes import auth, llm, user

app.register_blueprint(auth.bp)
app.register_blueprint(llm.bp)
app.register_blueprint(user.bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
