from apps.cms.model import User,Role,cms_role_user
from settings import sess
def add_role():
    r=Role(rolename='个人中心',roledesc='个人中心管理员',permissions=1)
    sess.add(r)
    sess.commit()
def add_user():
    user=User(username='zhangsan',password='123456',email='zhangsan@qq.com')
    sess.add(user)
    sess.commit()
def add(user_id,role_id):
    u = sess.query(User).filter(User.id==user_id).first()
    print(u)
    r = sess.query(Role).filter(Role.id==role_id).first()
    u.roles.append(r)
    sess.commit()


if __name__ == '__main__':
     #add_role()
    #add_user()
    add(1,1)

