import json

from flask import Blueprint, request, make_response, jsonify, Response

from api_lib.flask_pydantic.core import decorate
from app.model.user import User
from app.model.user_view_model import Login, ZhuCe

admin = Blueprint('admin', __name__)


def to__response(data, status_code: int = 200, just_str: bool = False) -> Response:
    if isinstance(data, Response):
        return data
    if not status_code:
        status_code = 200
    if status_code == 500 and isinstance(data, str):
        datas = {
            'error': data,
            'message': '服务器异常'
        }
    elif (400 <= status_code < 500) and isinstance(data, str):
        datas = {'mseeage': data}
    elif just_str and isinstance(data, str):
        return make_response(data, status_code)
    elif status_code == 200 and isinstance(data, str) and not just_str:
        datas = {'message': data}
    else:
        datas = data
    if just_str:
        return make_response(datas, status_code)
    resp = make_response(jsonify(datas), status_code)
    return resp


# 登录
@admin.route('login', methods=['POST'])
@decorate
def get_user_log(body_model: Login):
    r, s = User.login(body_model)
    return to__response(r, s)


# 注册
@admin.route('zhuce', methods=['POST'])
@decorate
def upload_user(body_model: ZhuCe):
    r, s = User.zhuce(body_model)
    return to__response(r, s)
