from flask import Blueprint
from flask_restful import Api

from api.v1.authorizate import Authorizate
from api.v1.history import History
from api.v1.login import Login
from api.v1.permission import Permission
from api.v1.permission_object import PermissionObject
from api.v1.permission_objects import PermissionObjects
from api.v1.permissions import Permissions
from api.v1.refresh import Refresh
from api.v1.registration import Registration
from api.v1.role import Role
from api.v1.roles import Roles
from api.v1.user import User
from api.v1.user_role import UserRole
from api.v1.user_roles import UserRoles
from api.v1.users import Users

v1_vp = Blueprint("v1", __name__, url_prefix="/v1")

api_v1 = Api(v1_vp)
api_v1.add_resource(Authorizate, "/authorizate")
api_v1.add_resource(History, "/history")
api_v1.add_resource(Login, "/login")
api_v1.add_resource(Permission, "/permission/<id>")
api_v1.add_resource(Permissions, "/permissions")
api_v1.add_resource(PermissionObject, "/permission_object/<name>")
api_v1.add_resource(PermissionObjects, "/permission_objects")
api_v1.add_resource(Refresh, "/refresh")
api_v1.add_resource(Registration, "/registration")
api_v1.add_resource(Role, "/role/<name>")
api_v1.add_resource(Roles, "/roles")
api_v1.add_resource(User, "/user/<name>")
api_v1.add_resource(Users, "/users")
api_v1.add_resource(UserRole, "/user_role/<id>")
api_v1.add_resource(UserRoles, "/user_roles")
