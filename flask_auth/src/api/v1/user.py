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
from utils.auth.utils import RequestParser
from utils.passwords.service import PasswordManager

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class User(Resource):

    decorators = [session]

    def get(self, name, session):
        """
        Getting User details
        ---
        parameters:
        - in: path
          description: User's username
          name: name
          type: string
          required: true
        responses:
          200:
            schema:
              properties:
                id:
                  type: string
                username:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", f"api/v1/user/{name}", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            if not what_to_do.is_anonim:
                if BaseRoles.ANONIMOUS.value not in what_to_do.get_roles_str():
                    query = session.query(UserDB).filter_by(username=name)
                    user = session.execute(query).one()
                    user = user[0].serialize()
                    if user["id"] == str(what_to_do.is_anonim.user_id):
                        return user, HTTPStatus.OK
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

    def put(self, name, session):
        """
        Changing User details
        ---
        parameters:
        - in: path
          description: User's username
          name: name
          type: string
          required: true
        - in: body
          description: User object
          schema:
            type: object
            required:
              - id
              - username
            properties:
              id:
                type: string
              username:
                type: string
              password:
                type: string
        responses:
          200:
            description: Updated User
            schema:
              properties:
                id:
                  type: string
                username:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "put", f"api/v1/user/{name}", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            user_id = auth.get_user_id()
            if not what_to_do.is_anonim:
                if BaseRoles.ANONIMOUS.value not in what_to_do.get_roles_str():
                    query = session.query(UserDB).filter_by(username=name)
                    user = session.execute(query).one()[0]
                    if str(user.id) == str(user_id):
                        need_to_commit = False
                        for property in data:
                            if hasattr(UserDB, property) and property != "_password" and property != "password":
                                query.update({property: data[property]})
                                need_to_commit = True
                            elif property == "password":
                                password = PasswordManager.generate_hash(password=data[property])
                                query.update({"password": password})
                        if need_to_commit:
                            session.commit()
                        user_serialize = user.serialize()
                        return user_serialize, HTTPStatus.OK
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

    def delete(self, name, session):
        """
        User Delete
        ---
        parameters:
        - in: path
          description: User's username
          name: name
          type: string
          required: true
        responses:
          200:
            description: User Deleted
            schema:
              properties:
                result:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(request, parser, "delete", f"api/v1/user/{name}", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            user_id = auth.get_user_id()
            if not what_to_do.is_anonim:
                if BaseRoles.ANONIMOUS.value not in what_to_do.get_roles_str():
                    query = session.query(UserDB).filter_by(username=name)
                    user = session.execute(query).one()[0]
                    if str(user.id) == str(user_id):
                        for role in what_to_do.roles:
                            session.query(UserRole).filter_by(user_id=str(user.id), role_id=str(role)).delete()
                        query.delete()
                        session.commit()
                        return {"result": f"User {name} has been deleted"}, HTTPStatus.OK
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
