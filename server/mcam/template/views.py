from urllib.request import urlopen

from flask import request
from flask_restful import Resource, reqparse
from mongoengine.errors import OperationError, NotUniqueError

from mcam.auth.utils import required_admin, authenticated
from mcam.provider.models import Provider
from mcam.template.models import Template

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('desc_image', type=urlopen)
parser.add_argument('providers', required=True, location="json", action="append")
parser.add_argument('resources', type=str, required=True)
parser.add_argument('outputs', type=str)
parser.add_argument('variables', type=str)
parser.add_argument('datasources', type=str)
parser.add_argument('user_variables', required=False, type=dict, location="json", action="append", store_missing=False)

update_parser = reqparse.RequestParser()
update_parser.add_argument('desc_image', type=urlopen, required=False, store_missing=False)
update_parser.add_argument('user_variables', required=False, type=dict, location="json", action="append",
                           store_missing=False)


class TemplateResource(Resource):
    @authenticated
    @required_admin
    def get(self, template_id):
        template_obj = Template.objects.get_or_404(id=template_id)
        return template_obj.to_dict()

    @authenticated
    @required_admin
    def patch(self, template_id):
        template_obj = Template.objects.get_or_404(id=template_id)
        request.get_json(force=True)
        parser_args = update_parser.parse_args()
        if parser_args.desc_image:
            template_obj.desc_image.replace(parser_args.desc_image)
            parser_args.pop('desc_image')
            template_obj.save()
        template_obj.update(**parser_args)
        template_obj.reload()
        return template_obj.to_dict()

    @authenticated
    @required_admin
    def delete(self, template_id):
        try:
            template_obj = Template.objects.get_or_404(id=template_id)
            template_obj.delete()
        except OperationError:
            return dict(message='could not delete  (Instance refers to it)'), 409
        return dict(message='deleted')


class TemplateListResource(Resource):
    @authenticated
    @required_admin
    def get(self):
        return [_.to_dict() for _ in Template.objects]

    @authenticated
    @required_admin
    def post(self):
        request.get_json(force=True)
        parser_args = parser.parse_args()
        for provider_id in parser_args.providers:
            Provider.objects.get_or_404(id=provider_id)
        desc_image = parser_args.pop('desc_image')
        template_obj = Template(**parser_args)
        is_ok, err = template_obj.validate_syntax()
        if not is_ok:
            return dict(message=f'validate error: {err}'), 409
        template_obj.desc_image.replace(desc_image)
        try:
            template_obj.save()
        except NotUniqueError:
            return dict(message='template name already exists'), 409
        return template_obj.to_dict()
