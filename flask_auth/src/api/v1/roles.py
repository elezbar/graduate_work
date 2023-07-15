from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from db.alchemy import session
from models.models import Role
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Roles(Resource):

    decorators = [session]

    def get(self, session):
        """
        Getting list of roles
        ---
        responses:
          200:
            description: Roles list
            schema:
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", "api/v1/roles", ["role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(Role)
                    roles = session.execute(query).all()
                    result = []
                    for user in roles:
                        uu = user[0].serialize()
                        result.append(uu)
                    return result, HTTPStatus.OK
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

    def post(self, session):
        """
        Creating Role
        ---
        parameters:
        - in: body
          description: Role object
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
        responses:
          200:
            description: Created Role
            schema:
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "api/v1/roles", ["role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(Role).filter_by(name=data["name"])
                    objs = session.query(query.exists())
                    objs = session.execute(objs)
                    if not objs.first()[0]:
                        role = Role(name=data["name"])
                        session.add(role)
                        session.commit()
                        return {"id": str(role.id), "name": f'{data["name"]}'}, HTTPStatus.CREATED
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
