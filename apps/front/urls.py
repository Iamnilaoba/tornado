import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
from apps.front.forms import *
import json
from apps.common.basert import *
from settings import sess
import string
import random
from dysms_python.demo_sms_send import send_sms
from io import BytesIO
from apps.common.captcha.xtcaptcha import Captcha


BASE=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tornado.options import define,options
define("port",default=8000,type=int,help="i love you")

# 登录
class sininHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("front/signin.html")

    def post(self, *args, **kwargs):
        fm = SigninFrom(self.request.arguments)
        if fm.validate():
            user = sess.query(FrontUser).filter(FrontUser.telephone==fm.telephone.data).first()
            if not user:
                return self.write(json.dumps(respParamErr("电话号码未注册")))
            r=user.checkPwd(fm.password.data)
            if r:
                return self.write(json.dumps(reSuccess("登陆成功")))
            else:
                return self.write(json.dumps(respParamErr("密码错误")))
        else:
            return self.write(json.dumps(respParamErr(fm.errmsg)))

# 注册
class sinupHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("front/singup.html")

    def post(self, *args, **kwargs):
        fm = SignupFrom(self.request.arguments)
        if fm.validate():
            u = FrontUser(telephone=fm.telephone.data,
                          username=fm.username.data,
                          password=fm.password.data)
            sess.add(u)
            sess.commit()
            delete(fm.telephone.data)
            return self.write(json.dumps(reSuccess("注册成功")))
        else:
            return self.write(json.dumps(respParamErr(fm.errmsg)))

# 发送短信验证码
class sendSMScode(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = SendSmsCodeForm(self.request.arguments)
        if fm.validate():
            source = string.digits
            source = ''.join(random.sample(source,4))
            send_sms(phone_numbers=fm.telephone.data,smscode=source)
            saveCache(fm.telephone.data,source,30*60)
            return self.write(json.dumps(reSuccess("发送成功")))
        else:
            return self.write(json.dumps(respParamErr(fm.errmsg)))


#  图片验证码
class imgcode(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        text, img = Captcha.gene_code()  # 生成数字和背景图
        print(text)  # 在服务器中打印出生成的验证码
        out = BytesIO()
        img.save(out, 'png')
        out.seek(0)
        saveCache(text, text, 60)  # 60秒有效时
        self.write(out.getvalue())


# 找回密码
class fwdHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("front/findpwd.html")

    def post(self, *args, **kwargs):
        fm = FindpwdForm(self.request.arguments)
        if fm.validate():
            r = sess.query(FrontUser).filter(FrontUser.telephone==fm.telephone.data)
            r.password = fm.password.data
            sess.commit()
            return self.write(json.dumps(reSuccess("密码修改成功")))
        else:
            return self.write(json.dumps(respParamErr(fm.errmsg)))

# 找回密码验证码
class sendpwdcode(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = SendCodeForm(self.request.arguments)
        if fm.validate():
            source = string.digits
            source = ''.join(random.sample(source,4))
            send_sms(phone_numbers=fm.telephone.data,smscode=source)
            saveCache(fm.telephone.data,source,30*60)
            return self.write(json.dumps(reSuccess("发送成功")))
        else:
            return self.write(json.dumps(respParamErr(fm.errmsg)))

# 登录·首页
class indexHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # banners = sess.query(Bander).order_by(Bander.priority.desc()).limit(3)
        # banks = sess.query(Boarder).all()
        # bank_id = self.get_argument('bank_id')
        self.render("front/base.html")



if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/sinin/',sininHandle),
                  (r'/sinup/',sinupHandle),
                  (r'/send_sms_code/',sendSMScode),
                  (r'/img_code/',imgcode),
                  (r'/',indexHandle),
                  (r'/findpwd/',fwdHandle),
                  (r'/sen_code/',sendpwdcode)],
        template_path=os.path.join(BASE, 'templates'),
        static_path=os.path.join(BASE, 'static'))
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

