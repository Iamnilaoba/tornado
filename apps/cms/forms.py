import wtforms
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms_tornado import Form
from ..common.model import Bander,Boarder
from settings import sess


class Baseform(Form):
    @property
    def errmsg(self):
        return self.errors.popitem()[1][0]


class UserForm(Baseform):
    email = wtforms.StringField(
        validators=[validators.Email(message='必须为邮箱'), validators.InputRequired(message='邮箱名不能为空')])
    password = wtforms.StringField(
        validators=[validators.InputRequired(message="密码不能为空"), validators.Length(min=6, max=50, message="长度为6-50位")])


class RestipwdForm(Baseform):
    oldpwd = wtforms.StringField(validators=[validators.InputRequired(message="不能为空,原密码错误")])
    newpwd = wtforms.StringField(validators=[validators.InputRequired(message="不能为空")])
    newpwd1 = wtforms.StringField(validators=[validators.EqualTo("newpwd", message="两次密码必须一致")])


class ResetEmailSendCode(Baseform):
    email = wtforms.StringField(
        validators=[validators.Email(message="必须为邮箱"), validators.InputRequired(message=" 邮箱不能为空")])


class ResetEmailForm(Baseform):
    email = wtforms.StringField(
        validators=[validators.Email(message="必须为邮箱"), validators.InputRequired(message=" 邮箱不能为空")])
    emailcode = wtforms.StringField(
        validators=[validators.InputRequired(message="验证码不能为空"), validators.Length(min=6, max=6, message="必须为六位")])


class BanderForm(Baseform):
    bannerName = wtforms.StringField(validators=[validators.InputRequired(message='必须输入名称')])
    imglink = wtforms.StringField(
        validators=[validators.URL(message="必须为url地址"), validators.InputRequired(message="不能为空")])
    link = wtforms.StringField(
        validators=[validators.URL(message="必须为url地址"), validators.InputRequired(message="不能为空")])
    priority = wtforms.IntegerField(validators=[validators.InputRequired(message="必须输入优先级")])

    def validate_imglink(self, filed):
        r = sess.query(Bander).filter(Bander.imglink == filed.data).first()
        if r:
            raise ValidationError('图片的url已存在，请勿重复添加 ' + str(r.id) + r.bannerName)

class BannerUpdate(BanderForm):
    id = wtforms.IntegerField(validators=[validators.InputRequired(message="请传入id")])

    def validate_imglink(self, filed):
        pass

    def validate_link(self, filed):
        pass


class BankForm(Baseform):
    bankname = wtforms.StringField(validators=[validators.InputRequired(message="不能为空")])
    def validate_bankname(self, filed):
        r = sess.query(Boarder).filter(Boarder.boarderName==filed.data).first()
        if r:
            raise ValidationError('名称不能重复 ')

class BankUpdate(BankForm):
    id = wtforms.IntegerField(validators=[validators.InputRequired(message="请传入id")])

    def validate_bankname(self, filed):
        pass
