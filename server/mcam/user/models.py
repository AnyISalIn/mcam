from mongoengine import fields
from werkzeug.security import generate_password_hash, check_password_hash

from mcam import db


class User(db.Document):
    username = fields.StringField(required=True, unique=True)
    password = fields.StringField(required=True)
    is_admin = fields.BooleanField(default=False)

    def to_dict(self):
        return dict(
            id=str(self.id),
            username=self.username,
            is_admin=self.is_admin
        )

    def __repr__(self):
        return f'<User: {self.username}>'

    def clean(self):
        if not self.password.startswith('pbkdf2'):
            self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
