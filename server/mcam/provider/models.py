from mongoengine import fields

from mcam import db


class Provider(db.Document):
    name = fields.StringField(unique=True, required=True)
    tags = fields.ListField()
    config = fields.StringField(required=True)

    def to_dict(self):
        return dict(
            id=str(self.id),
            name=self.name,
            tags=self.tags,
            config=self.config
        )

    def __repr__(self):
        return f'<Provider: {self.name}>'
