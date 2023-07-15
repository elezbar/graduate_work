from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc, select

from core.logger import get_logger
from db.alchemy import session
from models.models import Role, User
from models.models import UserRole as UserRoleDB
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class UserRoles(Resource):

    decorators = [session]

    def get(self, session):
        """
        Users Roles List
        ---
        parameters:
        - in: query
          description: Role's name
          name: role_name
          schema:
            type: string
        - in: query
          description: Users's username
          name: username
          schema:
            type: string
        responses:
          200:
            description: Users Roles List
            schema:
              properties:
                user_id:
                  type: number
                role_id:
                  type: number
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", "api/v1/user_roles", ["user_role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    role_name = request.args.get("role_name", default=None, type=str)
                    username = request.args.get("username", default=None, type=str)
                    query = select(UserRoleDB.id, User.id, User.username, Role.id, Role.name).join(User).join(Role)
                    if role_name:
                        query = query.filter(Role.name == role_name)
                    if username:
                        query = query.filter(User.username == username)
                    user_roles = session.execute(query).all()
                    result = []
                    for user_role in user_roles:
                        uu = {
                            "id": str(user_role[0]),
                            "user_id": str(user_role[1]),
                            "username": user_role[2],
                            "role_id": str(user_role[3]),
                            "role_name": user_role[4],
                        }
                        result.append(uu)
                    return result, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"UserRole not found: {e}")
            abort(HTTPStatus.NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)

    def post(self, session):
        """
        Adding role to the user
        ---
        parameters:
        - in: body
          description: User Role object
          schema:
            type: object
            required:
              - user_id
              - role_id
            properties:
              user_id:
                type: string
              role_id:
                type: string
        responses:
          200:
            description: New User Role
            schema:
              properties:
                id:
                  type: string
                user_id:
                  type: string
                role_id:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "api/v1/user_roles", ["user_role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(UserRoleDB).filter_by(user_id=data["user_id"], role_id=data["role_id"])
                    objs = session.query(query.exists())
                    objs = session.execute(objs)
                    if not objs.first()[0]:
                        role = UserRoleDB(user_id=data["user_id"], role_id=data["role_id"])
                        session.add(role)
                        session.commit()
                        return {"id": str(role.id), "user_id": data["user_id"], "role_id": data["role_id"]}, HTTPStatus.CREATED
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
