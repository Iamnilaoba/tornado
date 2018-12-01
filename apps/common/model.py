from datetime import datetime

from sqlalchemy import Column,String,Integer,Boolean,Text,ForeignKey,DateTime #内置的创建类的方法属性
from sqlalchemy.orm import relationship,backref
from settings import Base
import shortuuid


class Bander(Base):
    __tablename__ = 'bander'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bannerName = Column(String(20), nullable=False)
    imglink =Column(String(200), nullable=False, unique=True)
    link = Column(String(200), nullable=False, unique=True)
    priority = Column(Integer, default=1)

class Boarder(Base):
    __tablename__='boarder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    boarderName=Column(String(20), nullable=False)
    postnum=Column(Integer ,default=0)
    create_time=Column(DateTime,default=datetime.now)


class Post(Base) :
    __tablename__ = "common_post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    bank_id = Column(Integer, ForeignKey('boarder.id'))
    bank = relationship('Boarder', backref='posts') #关联bank表
    # 前台用户id使用的short_uuid, 类型和长度，约束必须一直
    user_id =Column(String(100), ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = relationship('FrontUser', backref='posts') # orm查询的时候使用
    readCount=Column(Integer,default=0) #浏览量

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id=Column(Integer,ForeignKey('common_post.id'))
    post=relationship('Post',backref=backref('tag',uselist=False))
    status = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now)


class Common(Base):
    __tablename__ = "common_common"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer,ForeignKey('common_post.id'))
    post = relationship('Post',backref='commons')
    user_id = Column(String(100),ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = relationship('FrontUser', backref='commons')  # orm查询的时候使用
    create_time = Column(DateTime, default=datetime.now)


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
