from app.model.user_db_model import UserDb
from app.model.user_view_model import Login, ZhuCe


class User:

    @staticmethod
    def login(body_model: Login):
        user = UserDb.query.filter(UserDb.user_name == body_model.user_name).first()
        if not user:
            return '未找到用户', 400
        if user.password != body_model.password:
            return '密码不正确', 400
        return user.dc, 200

    @staticmethod
    def zhuce(body_model: ZhuCe):
        if not User.auth_token(body_model.token, body_model.phone):
            return "验证码不正确", 400
        if UserDb.create(**body_model.dict()):
            user = UserDb.query.filter(UserDb.user_name == body_model.user_name).first()
            return user.dc, 200
        return "未知错误",500

    @staticmethod
    def auth_token(token, phone):
        """
        校验验证码
        :param token:
        :return:
        """
        return True

    @staticmethod
    def send_mns(phone_num):
        """
        通过jwt的库，对手机号做加盐，
        生成token
        :param phone_num:
        :return:
        """
        token = ""
        return token
