from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pswd = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Float, nullable=False, default=22.5)
    screen = db.Column(db.Float, nullable=False, default=50.0)
    room = db.Column(db.Integer, nullable=False, default=500.0)

    def __repr__(self):
        return f"Users('{self.username})'"

