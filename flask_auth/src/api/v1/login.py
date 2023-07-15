from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc, text

from core.logger import get_logger
from db.alchemy import session
from db.cache import Redis, get_redis
from models.models import User
from utils.auth.authentication import Authentication, AuthenticationManager
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser
from utils.passwords.service import PasswordManager
from utils.token.service import TokenManager, TokenType

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class Login(Resource):

    decorators = [session]

    def post(self, session):
        """
        User identification
        ---
        parameters:
        - in: body
          description: Request for user identification
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
            description: Pair of tokens
            schema:
              id: login
              properties:
                access:
                  type: string
                refresh:
                  type: string
        """
        try:
            data, args = RequestParser.request_pre_parser(request, parser, "post", "api/v1/login", ["user"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            is_auth = Authorization(what_to_do)
            if is_auth.is_authorise():
                user = session.query(User).filter_by(username=data["username"]).one()
                if PasswordManager.check_hash(user.password, data["password"]):
                    sql = text(
                        "SELECT role.id FROM role JOIN user_role ON "
                        "role.id = user_role.role_id WHERE "
                        "user_role.user_id = :user_id;"
                    )
                    roles = session.execute(sql, {'user_id': str(user.id)}).all()
                    roles_list = []
                    for role in roles:
                        roles_list.append(str(role[0]))
                    payload = {"user_id": str(user.id), "roles": ", ".join(roles_list)}
                    token_pair = {
                        "access": TokenManager(TokenType.ACCESS).encode(payload),
                        "refresh": TokenManager(TokenType.REFRESH).encode(payload),
                    }
                    fingerprint = auth.request_parser.get_fingerprint()
                    AuthenticationManager.save_refresh_token(
                        token_pair["refresh"], str(user.id), fingerprint, Redis(get_redis())
                    )
                    return token_pair, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"User not found: {e}")
            abort(HTTPStatus.UNAUTHORIZED)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
