from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from db.alchemy import session
from models.models import Role as RoleDB
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Role(Resource):

    decorators = [session]

    def get(self, name, session):
        """
        Getting information about a role
        ---
        parameters:
        - in: path
          description: Role name
          name: name
          type: string
          required: true
        responses:
          200:
            description: Role
            schema:
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", f"api/v1/role/{name}", ["role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(RoleDB).filter_by(name=name)
                    role = session.execute(query).one()
                    role = role[0].serialize()
                    return role, HTTPStatus.OK
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
        Deleting a role
        ---
        parameters:
        - in: path
          description: Role name
          name: name
          type: string
          required: true
        responses:
          200:
            description: Role Deleted
            schema:
              properties:
                result:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "delete", f"api/v1/role/{name}", ["role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    session.query(RoleDB).filter_by(name=name).delete()
                    session.commit()
                    return {"result": f"Role {name} has been deleted"}, HTTPStatus.OK
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
        Changing role
        ---
        parameters:
        - in: path
          description: Role name
          name: name
          type: string
          required: true
        - in: body
          name: permission
          description: Role object
          schema:
            type: object
            required:
              - id
              - name
            properties:
              id:
                type: string
              name:
                type: string
        responses:
          200:
            description: Changing Role
            schema:
              id: role_put
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "put", f"api/v1/role/{name}", ["role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(RoleDB).filter_by(name=name)
                    role = session.execute(query).one()[0]
                    need_to_commit = False
                    for property in data:
                        if hasattr(RoleDB, property):
                            query.update({property: data[property]})
                            need_to_commit = True
                    if need_to_commit:
                        session.commit()
                    role_serialize = role.serialize()
                    return role_serialize, HTTPStatus.OK
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
