from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.config import config
from core.logger import get_logger
from db.alchemy import session
from models.models import Permission
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import AuthorizationManager, RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Permissions(Resource):

    decorators = [session]

    def get(self, session):
        """
        Getting permissions list
        ---
        responses:
          200:
            description: List of permissions
            schema:
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
            _, args = RequestParser.request_pre_parser(None, parser, "get", "api/v1/permissions", ["permission"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(Permission)
                    perms = session.execute(query).all()
                    result = []
                    for perm in perms:
                        pp = perm[0].serialize()
                        result.append(pp)
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
        Creating permission
        ---
        parameters:
        - in: body
          description: Permission object
          schema:
            type: object
            required:
              - permission_object_id
              - role_id
              - permitted_action
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
            description: Created Permission
            schema:
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
                request, parser, "post", "api/v1/permissions", ["permission"]
            )
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    query = session.query(Permission).filter_by(
                        permission_object_id=data["permission_object_id"],
                        role_id=data["role_id"],
                        permitted_action=data["permitted_action"],
                        object_id=data["object_id"],
                    )
                    objs = session.query(query.exists())
                    objs = session.execute(objs)
                    if not objs.first()[0]:
                        perm = Permission(
                            permission_object_id=data["permission_object_id"],
                            role_id=data["role_id"],
                            permitted_action=data["permitted_action"],
                            object_id=data["object_id"],
                        )
                        session.add(perm)
                        session.commit()
                        AuthorizationManager.cache_clean(f"{config.cache.cache_prefix_to_find}")
                        return {
                            "id": str(perm.id),
                            "permission_object_id": data["permission_object_id"],
                            "role_id": data["role_id"],
                            "permitted_action": data["permitted_action"],
                            "object_id": data["object_id"],
                        }, HTTPStatus.CREATED
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
