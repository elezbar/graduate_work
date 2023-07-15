from http import HTTPStatus

from flask import abort
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.config import BaseRoles
from core.logger import get_logger
from utils.auth.authentication import Authentication
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Refresh(Resource):
    def get(self):
        """
        Refresh token pair
        ---
        responses:
          200:
            description: Refreshed token pair
            schema:
              properties:
                access:
                  type: string
                  description: Access Token
                refresh:
                  type: string
                  description: Access Token
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get", "api/v1/refresh", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            if not what_to_do.is_anonim:
                if BaseRoles.ANONIMOUS.value not in what_to_do.is_anonim.get_roles_str():
                    token_pair = auth.issue_token_pair()
                    if token_pair:
                        return token_pair, HTTPStatus.OK
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
