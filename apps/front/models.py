from settings import Base
from sqlalchemy import *
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid,datetime


class GenderEnum(Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(Base):
    __tablename__ = "front_user"
    id = Column(String(100), primary_key=True, default=shortuuid.uuid)
    telephone = Column(String(11), nullable=False, unique=True)
    username = Column(String(30), nullable=False)
    _password =Column(String(100), nullable=False)
    email = Column(String(50), unique=True)
    realname = Column(String(50))
    avatar = Column(String(100))  # 头像
    signature = Column(String(100))  # 签名
    gender = Column(String(20), default="男")
    join_time =Column(DateTime, default=datetime.datetime.now)

    # 因为要特殊处理password
    def __init__(self, password, **kwargs):
        self.password = password
        kwargs.pop('password', None)
        super(FrontUser, self).__init__(**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, frontpwd):
        # 1. 密码不希望外界访问 2.防止循环引用
        self._password = generate_password_hash(frontpwd)

    def checkPwd(self, frontpwd):
        # return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password, frontpwd)


if __name__ == '__main__':
    Base.metadata.create_all()





