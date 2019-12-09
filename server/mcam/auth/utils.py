import datetime
from functools import wraps

import jwt
from flask import request, current_app


def create_jwt_token(user_id):
    return jwt.encode(
        dict(user_id=user_id, exp=datetime.datetime.now() +
                                  datetime.timedelta(hours=24)),
        current_app.config['SECRET_KEY'], algorithm='HS256'
    ).decode()


def authenticated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from mcam.user.models import User
        try:
            token = request.headers.get('Authorization')
            if not token:
                return dict(message='please provider token'), 401
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithm='HS256'
            )
            user = User.objects.get_or_404(id=data['user_id'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return dict(message='token expire'), 401
        request.user = user
        return fn(*args, **kwargs)

    return wrapper


def required_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not request.user['is_admin']:
            return dict(message='require admin permission'), 403
        return fn(*args, **kwargs)

    return wrapper
