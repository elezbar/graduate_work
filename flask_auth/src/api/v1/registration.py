from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

import models
from core.config import BaseRoles
from core.logger import get_logger
from db.alchemy import session
from models.models import User
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser
from utils.passwords.service import PasswordManager

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Registration(Resource):

    decorators = [session]

    def post(self, session):
        """
        User Registration
        ---
        parameters:
        - in: body
          name: Registration
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
            description: A single user item
            schema:
              id: User
              properties:
                id:
                  type: string
                username:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "/api/v1/registration", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            is_auth = Authorization(what_to_do)
            if is_auth.is_authorise():
                query = session.query(User).filter_by(username=data["username"])
                objs = session.query(query.exists())
                objs = session.execute(objs)
                if not objs.first()[0]:
                    user = models.User(
                        username=data["username"], password=PasswordManager.generate_hash(password=data["password"])
                    )
                    session.add(user)
                    user_role = models.UserRole(user_id=user.id, role_id=BaseRoles.REGULAR.value)
                    session.add(user_role)
                    session.commit()
                    user_json = user.serialize()
                    return user_json, HTTPStatus.CREATED
                abort(HTTPStatus.UNAUTHORIZED)
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
