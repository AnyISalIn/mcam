from mcam import api

from . import views

api.add_resource(views.Auth, '/auth/login')
