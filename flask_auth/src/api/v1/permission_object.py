from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from db.alchemy import session
from models.models import Permission
from models.models import PermissionObject as PermissionObjectDB
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class PermissionObject(Resource):

    decorators = [session]

    def get(self, name, session):
        """
        Getting Permission object details
        ---
        parameters:
        - in: path
          description: Permission object name
          name: name
          type: string
          required: true
        responses:
          200:
            description: Permission object details
            schema:
              id: permission_object_get
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(
                None, parser, "get", f"api/v1/permission_object/{name}", ["permission_object"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionObjectDB).filter_by(name=name)
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
        Removing permission object
        ---
        parameters:
        - in: path
          description: Permission object name
          name: name
          type: string
          required: true
        responses:
          200:
            description: Permission has been removed
            schema:
              properties:
                result:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(
                None, parser, "delete", f"api/v1/permission_object/{name}", ["permission_object"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionObjectDB).filter_by(name=name)
                    perm_obj = session.execute(query).one()
                    perm_obj = perm_obj[0]
                    session.query(Permission).filter_by(permission_object_id=perm_obj.id).delete()
                    query.delete()
                    session.commit()
                    return {"result": f"Permission Object {name} has been deleted"}, HTTPStatus.OK
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
        Changing permission object
        ---
        parameters:
        - in: path
          description: Permission Object name
          name: name
          type: string
          required: true
        - in: body
          name: permission
          description: Permission object object
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
            description: Updated permission object
            schema:
              properties:
                id:
                  type: string
                name:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(
                request, parser, "put", f"api/v1/permission_object/{name}", ["permission_object"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionObjectDB).filter_by(name=name)
                    role = session.execute(query).one()[0]
                    need_to_commit = False
                    for property in data:
                        if hasattr(PermissionObjectDB, property):
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
