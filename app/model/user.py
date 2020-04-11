from app.model.user_db_model import UserDb
from app.model.user_view_model import Login, ZhuCe


class User:

    @staticmethod
    def login(body_model: Login):
        user = UserDb.query.filter(body_model.user_name).first()
        if not user:
            return '未找到用户', 400
        if user.password != body_model.password:
            return '密码不正确',400
        return user.dc,200

    @staticmethod
    def zhuce(body_model:ZhuCe):
        pass

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