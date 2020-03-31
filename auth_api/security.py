from functools import wraps
from flask import request, abort
from auth_api.models.user import UserModel


def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api_key')
        user_retrieved = UserModel.find_by_apikey(api_key)
        if user_retrieved:
            return view_function(*args, **kwargs)
        else:
            abort(401, 'Access denided. Invalid API key')
    return decorated_function


def mustbe_admin(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api_key')
        user_retrieved = UserModel.find_by_apikey(api_key)
        if user_retrieved.role == "admin":
            return view_function(*args, **kwargs)
        else:
            abort(401, 'Access denided. Must have admin privileges')
    return decorated_function

