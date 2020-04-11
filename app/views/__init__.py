from app import app
from app.views.articles import articles
from app.views.coupons import coupons
from app.views.product import product
from app.views.share import share
from app.views.view_user import user
from app.views.views import api_old
from app.views.voluntaries import voluntaries
from app.views.wechat import wechat_api
from app.views.admin import admin
from app.views.schools import schools
from app.views.auth import auth
from app.views.majors import majors
from app.views.ngk import ngk
from app.views.scores import scores
from app.views.message import message
from app.views.question import question
from app.views.paper import paper
from app.views.hook import hook
from app.views.v2_views.users import v2_user
from app.views.v2_views.schools import v2_school

# 这里分别给app注册了两个蓝图admin,user
# 参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
# 即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(api_old)
app.register_blueprint(hook)
app.register_blueprint(wechat_api, url_prefix='/api/wechat')
app.register_blueprint(admin, url_prefix='/api')
app.register_blueprint(user, url_prefix='/api/users')
app.register_blueprint(schools, url_prefix='/api/schools')
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(majors, url_prefix='/api/majors')
app.register_blueprint(ngk, url_prefix='/api/ngk')
app.register_blueprint(articles, url_prefix='/api/articles')
app.register_blueprint(voluntaries, url_prefix='/api/voluntaries')
app.register_blueprint(scores, url_prefix='/api/scores')
app.register_blueprint(message, url_prefix='/api/messages')
app.register_blueprint(coupons, url_prefix='/api/coupons')
app.register_blueprint(product, url_prefix='/api/product')
app.register_blueprint(question, url_prefix='/api/question')
app.register_blueprint(paper, url_prefix='/api/papers')
app.register_blueprint(share, url_prefix='/api/share')
app.register_blueprint(v2_user,url_prefix='/api/v2/users')
app.register_blueprint(v2_school,url_prefix='/api/v2/schools')