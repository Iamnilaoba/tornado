from sqlalchemy import create_engine # 创建引擎对象的模块
from sqlalchemy.orm import sessionmaker# 创建和数据库连接会话
from sqlalchemy.ext.declarative import declarative_base #基础类模块
import pymysql

# 连接数据库
pymysql.install_as_MySQLdb()
engine =create_engine('mysql://root:root@localhost/dd',
                      encoding='utf-8',echo=True)
# 创建会话对象
Session=sessionmaker(bind=engine)
sess=Session()

# 创建基类 （Base：创建数据表用的）
Base=declarative_base(bind=engine)



 # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1600566597@qq.com"  # 用户名
mail_pass = "zxwceaqigephbace"  # 口令


def sendmail(receivers,r):
    sender = '1600566597@qq.com'
    message = MIMEText('破茧科技更改邮箱验证码:'+r,'plain', 'utf-8')
    message['From'] = Header(sender,'utf-8')
    message['To'] = Header(receivers, 'utf-8')
    subject = '破茧科技更改邮箱验证码'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

#七牛云上传图片

