import tempfile
from base64 import b64encode

import delegator
from mongoengine import fields, DENY, EmbeddedDocument

from mcam import db
from mcam.provider.models import Provider
from mcam.service import TerraformManagerService, generate_plan_files

_terraform_service = None


def get_terraform_service():
    global _terraform_service
    if _terraform_service is None:
        return TerraformManagerService()
    return _terraform_service


class UserVariable(EmbeddedDocument):
    key = fields.StringField()
    required = fields.BooleanField(default=False)
    default = fields.StringField()

    def to_dict(self):
        return dict(
            key=self.key,
            required=self.required,
            default=self.default
        )


class Template(db.Document):
    name = fields.StringField(required=True, unique=True)
    desc_image = fields.ImageField()
    providers = fields.ListField(fields.ReferenceField(Provider, reverse_delete_rule=DENY))
    resources = fields.StringField(required=True)
    outputs = fields.StringField()
    variables = fields.StringField()
    user_variables = fields.EmbeddedDocumentListField(UserVariable)

    datasources = fields.StringField()

    def get_desc_image(self):
        bin_data = self.desc_image.read()
        if bin_data:
            return 'data:image/png;base64,' + b64encode(bin_data).decode()
        return None

    def to_dict(self):
        return dict(
            id=str(self.id),
            name=self.name,
            desc_image=self.get_desc_image(),
            providers=[{'id': str(_.id), 'name': _.name} for _ in self.providers],
            resources=self.resources,
            outputs=self.outputs,
            variables=self.variables,
            datasources=self.datasources,
            user_variables=[_.to_dict() for _ in self.user_variables]
        )

    def validate_syntax(self):
        with tempfile.TemporaryDirectory() as tempdir:
            generate_plan_files(tempdir,
                                self.providers,
                                self.resources,
                                self.outputs,
                                self.variables,
                                self.datasources)
            fake_init = ' '.join(get_terraform_service().init())
            delegator.run(f'{fake_init}', cwd=tempdir)
            validate_cmd = ' '.join(get_terraform_service().validate('-no-color'))
            cmd = delegator.run(f'{validate_cmd}', cwd=tempdir)
            if cmd.err:
                return False, cmd.err
            return True, None


def __repr__(self):
    return f'<Template: {self.name}>'
