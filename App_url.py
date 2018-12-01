import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from apps.cms.urls import *

from tornado.options import define,options
define("port",default=8000,help="i lo",type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/cms/', loginViewHandler),
                    (r'/cms/login/', loginHandler),
                    (r'/cms/index/', indexViewHandler),
                    (r'/cms/userinfo/', userInfoHandler),
                    (r"/cms/changepwd/", RegisterHandles),
                    (r'/cms/send_email_code/', ResetEmailSendCodeHandler),
                    (r'/cms/changeemail/', RegisterEmailHandler),
                    (r'/cms/banner/', BanderHandler),
                    (r'/cms/addbander/', addBannerHandler),
                    (r'/common/qiniu_token/', qiniutoken),
                    (r'/cms/deletebander/', deleteBannerHandle),
                    (r'/cms/updatebander/', updateBannerHandle),
                    (r'/cms/bank/', BankHandle),
                    (r'/cms/addbank/', addBankHandle),
                    (r'/cms/delebank/', deleteBankHandle),
                    (r'/cms/updatebank/', updateBankHandle)],
        template_path = os.path.join('templates'),
        static_path = os.path.join('static')
        settings = {

        }
        tornado.web.Application.__init__(self, handlers, **settings)



