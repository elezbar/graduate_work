from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Authorizate(Resource):
    def post(self):
        """
        Authorization request from an other service
        ---
        parameters:
        - in: body
          description: Authorization request from an other service
          schema:
            type: object
            required:
              - RequestedObjTypes
            properties:
              RequestedObjTypes:
                type: string
              RequestType:
                type: string
              RequestedObjId:
                type: string
        responses:
          200:
            description: Does the current user have the right to the requested resource
            schema:
              properties:
                is_authorise:
                  type: boolean
        """
        try:
            _, args = RequestParser.request_pre_parser(request, parser, None, "api/v1/authorizate", None)
            print(_, args)
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if authorization.is_authorise():
                return {"is_authorise": authorization.is_authorise()}, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"User not found: {e}")
            abort(HTTPStatus.NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.BAD_REQUEST)
