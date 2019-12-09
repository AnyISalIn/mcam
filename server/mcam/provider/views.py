from flask import request
from flask_restful import Resource, reqparse
from mongoengine.errors import OperationError, NotUniqueError

from mcam.auth.utils import required_admin, authenticated
from mcam.provider.models import Provider

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('tags', type=str, location="json", action="append")
parser.add_argument('config', type=str, required=True)

update_parser = reqparse.RequestParser()
update_parser.add_argument('name', type=str, required=False, store_missing=False)
update_parser.add_argument('tags', type=str, location="json", action="append", store_missing=False)
update_parser.add_argument('config', type=str, required=False, store_missing=False)


class ProviderResource(Resource):
    @authenticated
    @required_admin
    def get(self, provider_id):
        provider_obj = Provider.objects.get_or_404(id=provider_id)
        return provider_obj.to_dict()

    @authenticated
    @required_admin
    def delete(self, provider_id):
        try:
            provider_obj = Provider.objects.get_or_404(id=provider_id)
            provider_obj.delete()
        except OperationError:
            return dict(message='could not delete  (Template refers to it)'), 409

        return provider_obj.to_dict()

    @authenticated
    @required_admin
    def patch(self, provider_id):
        provider_obj = Provider.objects.get_or_404(id=provider_id)
        request.get_json(force=True)
        parser_args = update_parser.parse_args()
        provider_obj.update(**parser_args)
        return provider_obj.reload().to_dict()


class ProviderListResource(Resource):
    @authenticated
    @required_admin
    def get(self):
        return [_.to_dict() for _ in Provider.objects]

    @authenticated
    @required_admin
    def post(self):
        request.get_json(force=True)
        parser_args = parser.parse_args()
        try:
            provider_obj = Provider(**parser_args).save()
        except NotUniqueError:
            return dict(message='provider name already exists'), 409
        return provider_obj.to_dict()
