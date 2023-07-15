from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc, select

from core.logger import get_logger
from db.alchemy import session
from models.models import AuthHistory
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class History(Resource):

    decorators = [session]

    def get(self, session):
        """
        User's History List
        ---
        parameters:
        - in: query
          description: Page number
          name: page
          schema:
            type: number
        - in: query
          description: Limit items
          name: limit
          schema:
            type: number
        responses:
          200:
            description: User' s History List
            schema:
              properties:
                id:
                  type: string
                user_id:
                  type: string
                device:
                  type: string
                datetime:
                  type: string
                endpoint:
                  type: string
                action:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "get",
                                                       "api/v1/user_roles", ["user_role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    page = request.args.get("page", default=1, type=int)
                    limit = request.args.get("limit", default=20, type=int)
                    query = select(AuthHistory.id, AuthHistory.user_id, AuthHistory.device,
                                   AuthHistory.datetime, AuthHistory.endpoint,
                                   AuthHistory.action).offset(page * limit - limit).limit(limit)
                    auth_history = session.execute(query).all()
                    result = []
                    for history in auth_history:
                        hist = {
                            "id": str(history[0]),
                            "user_id": str(history[1]),
                            "device": str(history[2]),
                            "datetime": str(history[3]),
                            "endpoint": str(history[4]),
                            "action": str(history[5])
                        }
                        result.append(hist)
                    return result, HTTPStatus.OK
            abort(HTTPStatus.UNAUTHORIZED)
        except exc.IntegrityError as e:
            logger.error(f"Duplicate key value violates unique constraint: {e}")
            abort(HTTPStatus.CONFLICT)
        except exc.NoResultFound as e:
            logger.error(f"UserRole not found: {e}")
            abort(HTTPStatus.NOT_FOUND)
        except ValidationError as e:
            logger.error(f"Incorrect input data: {e}")
            abort(HTTPStatus.OK)
