from functools import wraps
from src.database import database
from flask_jwt_extended import get_jwt_identity
db = database.getConnection()
users = db.users
from flask import abort


class Roles:
    def roles_required(roles,message='Access denied: Insufficient role'):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                current_user = get_jwt_identity()
                user = users.find_one({'username': current_user})
                user_roles = user.get('roles', [])  # Assuming roles are stored as a list in the user document
                if any(role in user_roles for role in roles):
                    return fn(*args, **kwargs)
                else:
                    return {'message': message}, 403  # Forbidden
            return wrapper
        return decorator