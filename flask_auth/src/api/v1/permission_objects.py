from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from db.alchemy import session
from models.models import PermissionObject
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class PermissionObjects(Resource):

    decorators = [session]

    def get(self, session):
        """
        Getting Permission objects list
        ---
        responses:
          200:
            description: Permission objects
            schema:
              id: permission_objects_get
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(
                None, parser, "get", "api/v1/permission_objects", ["permission_object"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionObject)
                    perm_objs = session.execute(query).all()
                    result = []
                    for perm_obj in perm_objs:
                        po = perm_obj[0].serialize()
                        result.append(po)
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
        Creating permission object
        ---
        parameters:
        - in: body
          description: Permission Object object
          schema:
            type: object
            required:
              - permission_object_name
            properties:
              permission_object_name:
                type: string
        responses:
          200:
            description: Created permission object
            schema:
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(
                request, parser, "post", "api/v1/permission_objects", ["permission_object"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionObject).filter_by(name=data["name"])
                    objs = session.query(query.exists())
                    objs = session.execute(objs)
                    if not objs.first()[0]:
                        perm_obj = PermissionObject(name=data["name"])
                        session.add(perm_obj)
                        session.commit()
                        return {"id": str(perm_obj.id), "name": f'{data["name"]}'}, HTTPStatus.CREATED
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
