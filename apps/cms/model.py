from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column,String,Integer,Table,ForeignKey,DateTime #内置的创建类的方法属性
from settings import Base
from sqlalchemy.orm import relationship

class Permission:
    USER_INFO=1
    BANBER=2
    INVITATION=4
    COMMENT=8
    MODEL=16
    FORNT_USER=32
    CMS_USER=64
    CMS_USER_GROUP=128

cms_role_user=Table(
    "cms_role_user",
    Base.metadata,
    Column('cms_role_id',Integer, ForeignKey('role.id'), primary_key=True),
    Column('cms_user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(String(20), unique=True, nullable=False)
    roledesc=Column(String(200), unique=True, nullable=False)
    permissions = Column(Integer, default=Permission.USER_INFO)
    users=relationship("User",backref='roles',secondary=cms_role_user)



class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),unique=True,nullable=False)
    _password = Column(String(200),nullable=False) # 加密过的
    email = Column(String(30),unique=True,nullable=False)
    join_time = Column(DateTime,default=datetime.now)

    # 返回当前用户的权限
    @property
    def current_user_permission(self):
        '''获取当前用户的权限'''
        num = 0
        for role in self.roles:
            num = num | role.permissions

        return num

    # 校验用户是否拥有这个权限
    def checkpermission(self, permission):
        return self.current_user_permission & permission != 0

    # 因为要特殊处理password
    def __init__(self,password,**kwargs):
        self.password = password
        kwargs.pop('password',None)
        super(User,self).__init__(**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,frontpwd):
        # 1. 密码不希望外界访问 2.防止循环引用
        self._password = generate_password_hash(frontpwd)

    def checkPwd(self,frontpwd):
        #return self.password == generate_password_hash(frontpwd)
        return check_password_hash(self._password,frontpwd)
if __name__ == '__main__':
    Base.metadata.create_all()
