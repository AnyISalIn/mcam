from flask_restful import Resource, reqparse, request, current_app

from mcam.auth.utils import create_jwt_token
from mcam.user.models import User

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class Auth(Resource):
    def post(self):
        request.get_json(force=True)
        parser_args = parser.parse_args()

        user_obj = User.objects(username=parser_args.username).first()

        if user_obj and user_obj.check_password(parser_args.password):
            token = create_jwt_token(str(user_obj.id))
            ret = user_obj.to_dict()
            ret['token'] = token
            current_app.logger.debug(f'User {user_obj.username} Login Success')
            return ret
        return dict(message='用户名或密码错误'), 401
