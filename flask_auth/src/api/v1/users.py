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

    def post(self, session):
        """
        Getting list of users by id
        ---
         parameters:
        - in: body
          description: List id_users
          schema:
            type: object
            required:
              - id_users
              - username
            properties:
              id_users:
                type: list[string]
          200:
            description: Users list
            schema:
              id: Permissions
              properties:
                id:
                  type: string
                username:
                  type: string
                email:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "api/v1/users", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(UserDB)
                    if data and data.get('id_users'):
                        query = query.filter(UserDB.id.in_(data['id_users']))
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
