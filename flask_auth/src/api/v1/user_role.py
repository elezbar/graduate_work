from http import HTTPStatus

from flask import abort
from flask_restful import Resource, reqparse
from pydantic.error_wrappers import ValidationError
from sqlalchemy import exc

from core.logger import get_logger
from db.alchemy import session
from models.models import UserRole as UserRoleDB
from utils.auth.authentication import Authentication
from utils.auth.authorization import Authorization
from utils.auth.utils import RequestParser

logger = get_logger(__name__)
parser = reqparse.RequestParser()
parser.add_argument("User-Agent", location="headers")
parser.add_argument("Authorization", location="headers")


class UserRole(Resource):

    decorators = [session]

    def delete(self, id, session):
        """
        Removing User Role
        ---
        parameters:
        - in: path
          description: User Role id
          name: id
          type: string
          required: true
        responses:
          200:
            description: User Role has been removed
            schema:
              properties:
                result:
                  type: string
        """
        try:
            _, args = RequestParser.request_pre_parser(None, parser, "delete", f"api/v1/user_role/{id}", ["user_role"])
            auth = Authentication(args)
            what_to_do = auth.authenticate()
            authorization = Authorization(what_to_do)
            if not what_to_do.is_anonim:
                if authorization.is_authorise():
                    session.query(UserRoleDB).filter_by(id=id).delete()
                    session.commit()
                    return {"result": f"User Role {id} has been deleted"}, HTTPStatus.OK
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
