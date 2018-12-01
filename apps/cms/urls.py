from settings import sess, sendmail
from apps.cms.model import User, Role, cms_role_user
from apps.common.basert import *
from apps.common.model import *
from apps.cms.forms import UserForm,BankForm,BankUpdate, RestipwdForm, ResetEmailForm, ResetEmailSendCode, BanderForm,BannerUpdate
import string
import json
import random
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
import pymysql

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def coon():
    coon = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='dd', charset='utf8')


from tornado.options import define, options
define('port', default=8000, help='ok', type=int)



class loginViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cms/login.html')


class loginHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm=UserForm(self.request.arguments)
        if fm.validate():
            email=fm.email.data
            password=fm.password.data
            user=sess.query(User).filter(User.email==email).first()
            if user:
                if user.checkPwd(password):
                    self.set_secure_cookie('username', user.username)
                    self.write(json.dumps(reSuccess("登录成功")))
                else:  # 密码错误
                    self.write(json.dumps(respParamErr("密码错误")))
            else:
                self.write(json.dumps(respParamErr("用户名错误")))
        else:
            self.write(json.dumps(fm.errmsg))



class indexViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cms/cms_index.html')


class userInfoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        user = self.get_secure_cookie('username')
        user = sess.query(User).filter(User.username == user).first()
        self.render('cms/userinfo.html', user=user)


class RegisterHandles(tornado.web.RequestHandler):
    def get(self):
        self.render('cms/changepwd.html')

    def post(self, *args, **kwargs):
        fm = RestipwdForm(self.request.arguments)
        if fm.validate():
            user = self.get_secure_cookie('username')
            user = sess.query(User).filter(User.username == user).first()
            r = user.checkPwd(fm.oldpwd.data)
            if r:
                user.password = fm.newpwd.data
                sess.commit()
                self.write(json.dumps(reSuccess("修改密码成功")))
            else:
                self.write(json.dumps(respParamErr("旧密码错误")))
        else:
            self.write(json.dumps(fm.errors))


class RegisterEmailHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("cms/changeemail.html")  # 渲染模板

    def post(self):
        fm = ResetEmailForm(self.request.arguments)  # 判断是否能通过验证
        if fm.validate():
            username = self.get_secure_cookie('username')
            user = sess.query(User).filter(User.email == fm.email.data).first()  # 查看邮箱是否存在
            if user:
                self.write(json.dumps(respParamErr(msg="邮箱已注册")))
            else:
                emailcodeb = self.get_secure_cookie("emailcode")  #  发送时用set保存在cookie里，用户输入时用get从cookie取出对比
                emailcode = str(emailcodeb, 'utf-8')
                if not emailcode or emailcode != fm.emailcode.data:
                    self.write(json.dumps(respParamErr(msg="验证码错误")))
                else:
                    user = sess.query(User).filter(User.username == username).first()
                    user.email = fm.email.data
                    sess.commit()
                    self.write(json.dumps(reSuccess(msg="修改邮箱成功")))
        else:
            self.write(json.dumps(fm.errors))  # 通不过校验,返回错误


# 发送验证码
class ResetEmailSendCodeHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = ResetEmailSendCode(self.request.arguments)
        if fm.validate():
            user = sess.query(User).filter(User.email == fm.email.data).first()  # 查看邮箱是否存在
            if user:
                self.write(json.dumps(respParamErr(msg="邮箱已注册")))
            else:
                r = string.ascii_letters + string.digits  # 发送验证码
                r = ''.join(random.sample(r, 6))
                self.set_secure_cookie("emailcode", r)
                emailcode = fm.email.data
                sendmail(emailcode, r)
                print(r)
                self.write(json.dumps(reSuccess(msg='发送成功，请查看邮箱')))
        else:
            self.write(json.dumps(respParamErr(msg=fm.errmsg)))


# 轮播图
class BanderHandler(tornado.web.RequestHandler):
    def get(self):
        banners = sess.query(Bander).all()
        self.render('cms/bander.html', banners=banners)

# 添加轮播图
class addBannerHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = BanderForm(self.request.arguments)
        if fm.validate():
            bander = Bander(bannerName=fm.bannerName.data, imglink=fm.imglink.data,
                            link=fm.link.data, priority=fm.priority.data)
            sess.add(bander)
            sess.commit()
            self.write(json.dumps(reSuccess('添加成功')))
        else:
            self.write(json.dumps(respParamErr(msg=fm.errmsg)))

# 删除轮播图
class deleteBannerHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        banner_id = self.get_argument('id') # 获取到用户输入的id
        if not banner_id or not banner_id.isdigit():
            return self.write(json.dumps(respParamErr("请输入正确id")))
        banner = sess.query(Bander).filter(Bander.id == banner_id).first()  # 对比用户传入的id是否跟数据库里的id一样
        if banner:
            sess.delete(banner)
            sess.commit()
            return self.write(json.dumps(reSuccess("删除成功")))
        else:
            return self.write(json.dumps(respParamErr("请输入正确id")))

# 更新轮播图
class updateBannerHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = BannerUpdate(self.request.arguments)
        if fm.validate():
            bander = sess.query(Bander).filter(Bander.id == fm.id.data).first()
            if bander:
                bander.link = fm.link.data
                bander.imglink = fm.imglink.data
                bander.priority = fm.priority.data
                bander.bannerName = fm.bannerName.data
                sess.commit()
                return self.write(json.dumps(reSuccess('更新成功')))
            else:
                return self.write(json.dumps(respParamErr("请输入正的id")))
        else:
            return self.write(json.dumps(respParamErr("更新失败")))

# 板块管理
class BankHandle(tornado.web.RequestHandler):
    def get(self):
        banks = sess.query(Boarder).all()
        self.render("cms/bank.html",banks=banks)

# 添加板块
class addBankHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = BankForm(self.request.arguments)
        if fm.validate():
            bank = Boarder(boarderName=fm.bankname.data)
            sess.add(bank)
            sess.commit()
            return self.write(json.dumps(reSuccess("添加成功")))
        else:
            return self.write(json.dumps(respParamErr("添加失败")))

# 删除板块
class deleteBankHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        bank_id = self.get_argument("id")
        if not bank_id or not bank_id.isdigit():
            return self.write(json.dumps(respParamErr("请输入正确的id")))
        bank = sess.query(Boarder).filter(Boarder.id==bank_id).first()
        if bank:
            sess.delete(bank)
            sess.commit()
            return self.write(json.dumps(reSuccess("删除成功")))
        else:
            return self.write(json.dumps(respParamErr("没有该板块")))

# 更新板块
class updateBankHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        fm = BankUpdate(self.request.arguments)
        if fm.validate():
            bank = sess.query(Boarder).filter(Boarder.id==fm.id.data).first()
            if bank:
                bank.boarderName=fm.bankname.data
                sess.commit()
                return self.write(json.dumps(reSuccess("修改成功")))
            else:
                return self.write(json.dumps(respParamErr("id失效")))
        else:
            return self.write(json.dumps(respParamErr("没有该板块")))


# 帖子管理
class PostHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        posts = sess.query(Post).all()
        self.render("cms/postmgr.html",posts=posts)

# 帖子加精操作
class addTagHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        post_id = self.get_argument('post_id')
        post = sess.query(Post).filter(Post.id==post_id).first()
        if post:
            tag = Tag(post=post,status=True)
            sess.add(tag)
            sess.commit()
            return self.write(json.dumps(reSuccess("加精完成")))
        else:
            return self.write(json.dumps(respParamErr("请传入正确的id")))

# 取消加精
class deleteTagHandle(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        post_id = self.get_argument('post_id')
        tag = sess.query(Tag).filter(Tag.id==post_id).first()
        if tag:
            tag.status=False
            sess.commit()
            return self.write(json.dumps(reSuccess("取消完成")))
        else:
            return self.write(json.dumps(respParamErr("请传入正确的id")))





from qiniu import Auth
class qiniutoken(tornado.web.RequestHandler):
    def get(self):
        ak = "hvNEDY7K1pYh_hS0pGLGpztuHnE2UoAVcUTRHGYN"
        sk = "M_pJxubIeA71x6RoQ_Qk5mP55Gncy1Jks3qNalCn"
        q = Auth(ak, sk)
        bucket_name = 'pjbbs2'  # 仓库的名字
        token = q.upload_token(bucket_name)
        self.write(json.dumps({'uptoken': token}))


if __name__ == '__main__':
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    }
    tornado.options.parse_command_line()
    #app = Application()
    app = tornado.web.Application(
        handlers=[(r'/cms/', loginViewHandler),
                  (r'/cms/login/', loginHandler),
                  (r'/cms/index/', indexViewHandler),
                  (r'/cms/userinfo/', userInfoHandler),
                  (r"/cms/changepwd/", RegisterHandles),
                  (r'/cms/send_email_code/', ResetEmailSendCodeHandler),
                  (r'/cms/changeemail/', RegisterEmailHandler),
                  (r'/cms/banner/', BanderHandler),
                  (r'/cms/addbander/', addBannerHandler),
                  (r'/common/qiniu_token/', qiniutoken),
                  (r'/cms/deletebander/',deleteBannerHandle),
                  (r'/cms/updatebander/',updateBannerHandle),
                  (r'/cms/bank/',BankHandle),
                  (r'/cms/addbank/',addBankHandle),
                  (r'/cms/delebank/',deleteBankHandle),
                  (r'/cms/updatebank/',updateBankHandle),
                  (r'/cms/post/',PostHandle),
                  (r'/cms/addtag/',addTagHandle),
                  (r'/cms/deletetag/',deleteTagHandle)], **settings,
            template_path=os.path.join(BASE,'templates'),
            static_path=os.path.join(BASE,'static'))
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
