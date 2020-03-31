from flask import Flask, g, request, abort
from flask_httpauth import HTTPTokenAuth
from functools import wraps

app = Flask(__name__)
# auth = HTTPTokenAuth(scheme='Token')

users = [
    {'username':'juan', 'password':'juanpwd', 'apikey':'juankey'}
]

# @auth.verify_token
# def verify_token(token):
#     if token in tokens:
#         g.current_user = tokens[token]
#         return True
#     return False

def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') == users[0]['apikey']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.route('/')
@require_appkey
def index():
    print("here", request.headers.get('key'))
    return "Hello, %s!" % "Chava"


if __name__ == '__main__':
    app.run()
