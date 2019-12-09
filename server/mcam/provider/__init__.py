from mcam import api

from . import views

api.add_resource(views.ProviderResource, '/providers/<provider_id>')
api.add_resource(views.ProviderListResource, '/providers')
