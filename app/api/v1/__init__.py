from flask import Blueprint

from app.api.v1 import user,donar, wish ,FeedBack,Organization,Picture
def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__, static_folder='../../static', template_folder='../../templates')
    user.api.register(bp_v1)
    donar.api.register(bp_v1)
    wish.api.register(bp_v1)
    FeedBack.api.register(bp_v1)
    Organization.api.register(bp_v1)
    Picture.api.register(bp_v1)
    return bp_v1