from .extensions import db
import flask.ext.login as fel
import bcrypt

"""Add your models here."""


class User(db.Model, fel.UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    @property
    def links(self):
        return [link.shortlink for link in self.link]

    def __repr__(self):
        return "<User {}>".format(self.email)


class Link(db.Model):
    """user added urls"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    shortlink = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
