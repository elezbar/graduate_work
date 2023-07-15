from flask import Blueprint

from . import v1

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(v1.v1_vp)
