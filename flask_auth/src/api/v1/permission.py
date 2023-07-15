from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.config import config
from core.logger import get_logger
from db.alchemy import session
from models.models import Permission as PermissionDB
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import AuthorizationManager, RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Permission(Resource):

    decorators = [session]

    def get(self, id, session):
        """
        Getting Permission details
        ---
        parameters:
        - in: path
          description: Permission Id
          name: id
          type: string
          required: true
        responses:
          200:
            description: Permission details
            schema:
              id: permission_get
              properties:
                id:
                  type: string
                permission_object_id:
                  type: string
                role_id:
                  type: string
                permitted_action:
                  type: string
                object_id:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", f"api/v1/permission/{id}", ["permission"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionDB).filter_by(id=id)
                    perm = session.execute(query).one()[0].serialize()
                    return perm, HTTPStatus.OK
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

    def delete(self, id, session):
        """
        Removing permission
        ---
        parameters:
        - in: path
          description: Permission Id
          name: id
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
                None, parser, "delete", f"api/v1/permission/{id}", ["permission"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    session.query(PermissionDB).filter_by(id=id).delete()
                    session.commit()
                    AuthorizationManager.cache_clean(f"{config.cache.cache_prefix_to_find}")
                    return {"result": f"Permission {id} has been deleted"}, HTTPStatus.OK
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

    def put(self, id, session):
        """
        Changing permission
        ---
        parameters:
        - in: path
          description: Permission Id
          name: id
          type: string
          required: true
        - in: body
          description: Permission object
          schema:
            type: object
            required:
              - permission_object_id
              - role_id
              - permitted_action
              - object_id
            properties:
              permission_object_id:
                type: string
              role_id:
                type: string
              permitted_action:
                type: string
              object_id:
                type: string
        responses:
          200:
            description: Updated permission
            schema:
              id: permission_put
              properties:
                id:
                  type: string
                permission_object_id:
                  type: string
                role_id:
                  type: string
                permitted_action:
                  type: string
                object_id:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(
                request, parser, "put", f"api/v1/permission/{id}", ["permission"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(PermissionDB).filter_by(id=id)
                    perm = session.execute(query).one()[0]
                    need_to_commit = False
                    for property in data:
                        if hasattr(PermissionDB, property):
                            query.update({property: data[property]})
                            need_to_commit = True
                    if need_to_commit:
                        session.commit()
                        AuthorizationManager.cache_clean(f"{config.cache.cache_prefix_to_find}")
                    perm_serialize = perm.serialize()
                    return perm_serialize, HTTPStatus.OK
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
        except TypeError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
