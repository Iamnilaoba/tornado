import wtforms
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms_tornado import Form
from settings import sess
import hashlib
from apps.common.memcachedUtil import *
from apps.common.model import *



class Baseform(Form):
    @property
    def errmsg(self):
        return self.errors.popitem()[1][0]


class SigninFrom(Baseform):
    telephone=wtforms.StringField(validators=[validators.Regexp('^1[35678]\d{9}$',message='请输入正确的电话号码')])
    password=wtforms.StringField(validators=[validators.InputRequired(message='必须输入密码'),validators.Length(min=6,max=20,message='密码长度在6到20位')])


#发送验证码验证
class SendSmsCodeForm(Baseform):
    telephone = wtforms.StringField(validators=[validators.Regexp('^1[35786]\d{9}$',message='请输入正确电话号码')])
    sign = wtforms.StringField(validators=[validators.InputRequired(message="必须输入签名")])
    def validate_telephone(self,filed): # 如果手机号重复没必要发送验证码
        u = sess.query(FrontUser).filter(FrontUser.telephone == filed.data).first()
        if u :
            raise ValidationError('手机号已被注册')

    def validate_sign(self,filed):
        # 生成md5字符串
        sign = md5(self.telephone.data)
        if sign != filed.data :
            raise ValidationError('请输入正确的签名')

def md5(telephone):
    m = hashlib.md5()
    v = telephone + 'zhanghendenvpengyou'
    m.update(v.encode("utf-8"))
    r = m.hexdigest()
    return r


#注册验证
class SignupFrom(SendSmsCodeForm):
    username = wtforms.StringField(validators=[validators.InputRequired(message="必须输入用户名"),validators.Length(min=6,max=20,message="用户名必须是6-20位")])
    password = wtforms.StringField(validators=[validators.InputRequired(message="必须输入密码"),validators.Length(min=6,max=20,message="密码必须是6-20位")])
    password1 = wtforms.StringField(validators=[validators.EqualTo('password',message="两次密码必须一致")])
    smscode = wtforms.StringField(validators=[validators.InputRequired(message="必须输入手机验证码")])
    captchacode = wtforms.StringField(validators=[validators.InputRequired(message="必须输入图片验证码")])

    sign = wtforms.StringField()
    def validate_sign(self, filed):
        pass

    def validate_smscode(self,filed):
        smscode = getCache(self.telephone.data)
        if not smscode :
            raise ValidationError('请输入正确的手机验证码')
        if smscode.upper() != filed.data :
            raise ValidationError('请输入正确的手机验证码')

    def validate_captchacode(self,filed):
        if not getCache(filed.data):
            raise ValidationError('请输入正确的图片验证码')

    def validate_username(self,field):
        u = sess.query(FrontUser).filter(FrontUser.username == field.data).first()
        if u :
            raise ValidationError('用户名已存在')

class SendCodeForm(Baseform):
    telephone = wtforms.StringField(validators=[validators.Regexp('^1[35786]\d{9}$', message='请输入正确电话号码')])
    def validate_telephone(self, filed):
        r = sess.query(FrontUser).filter(FrontUser.telephone == filed.data).first()
        if not r:
            raise ValidationError('请输入正确的手机号')

class FindpwdForm(SendCodeForm):
    password = wtforms.StringField(validators=[validators.InputRequired(message="必须输入密码"), validators.Length(min=6, max=20, message="密码必须是6-20位")])
    password1 =wtforms.StringField(validators=[validators.EqualTo('password', message="两次密码必须一致")])
    smscode = wtforms.StringField(validators=[validators.InputRequired(message="必须输入手机验证码")])

    def validate_smscode(self, filed):
        # 从缓存中获取到，然后校验
        smscode = getCache(self.telephone.data)
        print("校验得到的验证码" + smscode)
        if not smscode:
            raise ValidationError('请输入正确的手机验证码')
        if smscode.upper() != filed.data:
            raise ValidationError('验证码错误')








