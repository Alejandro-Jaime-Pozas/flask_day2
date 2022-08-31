from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# create user class
class User(db.Model, UserMixin): # UserMixin allows the instance of User class to access get(), and other methods
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # ALWAYS store time to UTC time (universal central time) better to change on the frontend
    posts = db.relationship('Post', backref='author', lazy='dynamic') # creates a relationship bw post instance and its author; you can then access that author's username, email, etc

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # save the pswd as hashed version of the pswd
        self.set_password(kwargs['password']) # why not just input password?
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User: {self.username} | {self.email}"

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id) # get() converts integers to strings

# create Post class
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # ALWAYS store time to UTC time (universal central time) better to change on the frontend
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # the 'user' here refers to the table 'user', which is why lowercase; SQL = FOREIGN KEY(user_id) REFERENCES user(id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id} | {self.title}"

    # method to update title and/or body of the posts
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date_created": self.date_created,
            "user_id": self.user_id
        }

# to implement migrations folder, type cmd line >>> flask db init