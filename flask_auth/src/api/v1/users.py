from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.config import BaseRoles
from core.logger import get_logger
from db.alchemy import session
from models.models import User as UserDB
from models.models import UserRole
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser
from utils.passwords.service import PasswordManager

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Users(Resource):

    decorators = [session]

    def get(self, session):
        """
        Getting list of users
        ---
        responses:
          200:
            description: Users list
            schema:
              id: Permissions
              properties:
                id:
                  type: string
                username:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", "api/v1/user", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(UserDB)
                    users = session.execute(query).all()
                    result = []
                    for user in users:
                        uu = user[0].serialize()
                        result.append(uu)
                    return result, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"Users not found: {e}")
            abort(HTTPStatus.NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)

    def post(self, session):
        """
        Creating User
        ---
        parameters:
        - in: body
          description: User object
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
              password:
                type: string
        responses:
          200:
            description: Created User
            schema:
              properties:
                id:
                  type: string
                username:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "api/v1/user", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            if not what_to_do.is_anonim:
                if BaseRoles.SUPERUSER.value in what_to_do.get_roles_str():
                    query = session.query(UserDB).filter_by(username=data["username"])
                    objs = session.query(query.exists())
                    objs = session.execute(objs)
                    if not objs.first()[0]:
                        user = UserDB(
                            username=data["username"], password=PasswordManager.generate_hash(password=data["password"])
                        )
                        session.add(user)
                        session.commit()
                        user_role = UserRole(user_id=user.id, role_id=BaseRoles.REGULAR.value)
                        session.add(user_role)
                        session.commit()
                        return user.serialize(), HTTPStatus.CREATED
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"User not found: {e}")
            abort(HTTPStatus.NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
