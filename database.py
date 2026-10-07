from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    python = db.Column(db.Integer, nullable=False)
    mathematics = db.Column(db.Integer, nullable=False)
    communication = db.Column(db.Integer, nullable=False)
    design = db.Column(db.Integer, nullable=False)
    security = db.Column(db.Integer, nullable=False)
    ai = db.Column(db.Integer, nullable=False)

    predicted_career = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
