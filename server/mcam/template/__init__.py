from mcam import api

from . import views

api.add_resource(views.TemplateResource, '/templates/<template_id>')
api.add_resource(views.TemplateListResource, '/templates')
