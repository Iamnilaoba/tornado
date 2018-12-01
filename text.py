
 # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# # 第三方 SMTP 服务
# mail_host = "smtp.qq.com"  # 设置服务器
# mail_user = "2697015679@qq.com"  # 用户名
# mail_pass = "yrggyaebappydhac"  # 口令
#
# sender = '2697015679@qq.com'
# receivers = ['1600566597@qq.com']
# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['To'] = Header("测试", 'utf-8')
# '2|1:0|10:1543367151|8:username|12:emhhbmdzYW4=|a6f40741c14aa6979cdf5f49cdf15bb2d73acbe09762b073aa256b7f4b6b5986'
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')
#
# try:
#     smtpObj = smtplib.SMTP()
#     smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
#     smtpObj.login(mail_user, mail_pass)
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print("邮件发送成功")
# except smtplib.SMTPException:
#     print("Error: 无法发送邮件")

import base64, uuid
print(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))

b=b'E1a9ez'
s=str(b,'utf-8')
print(s)