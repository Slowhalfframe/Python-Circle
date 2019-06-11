import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from itsdangerous import TimedJSONWebSignatureSerializer


os.environ['DJANGO_SETTINGS_MODULE'] = 'second_Edition.settings'


def mail(user_email, id):
    SECRET_KEY = '3_&qbax4_(xf!%ahsbahn(*8%o2-_1rzm)zr@^nht8q-dwq09z'
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600*24)
    token = s.dumps({'confirm': id})
    token = token.decode('utf8')
    print(token)
    url = "http://www.ofus.ink/users/email_verification/{0}".format(token)
    # 发件人邮箱账号
    my_sender = '1441576268@qq.com'

    # 发件人邮箱密码 密码不是真正的密码是 授权码，授权码是用于登录第三方邮件客户端的专用密码。
    my_pass = 'szlcejiprutxbafa'

    # 收件人邮箱账号
    # my_user = '18569938068@163.com'
    my_user = user_email
    # print("开始填信")
    ret = True
    mail_msg = '<h1>欢迎您</h1>请点击下方链接进行验证邮箱<br><small>请在24小时内点击验证，过期无效</small><a href="{0}">点我进行验证</a>'.format(url)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["逼乎儿", my_sender])
    msg['To'] = formataddr(["尊敬的", my_user])
    msg['Subject'] = '逼乎儿(bihuer)--一股清流'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()
    print("end")
    ret = False
    return ret


def forget_email(user_email, id):
    SECRET_KEY = 's(do(h$i-d3rzrx7yhw@ik!cgwg+52-c#roc*3gk#wfk2y@1=2'
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600*0.5)
    token = s.dumps({'confirm': id})
    token = token.decode('utf8')
    print(token)
    url = "http://www.ofus.ink/users/forget_pwd/{0}".format(token)
    # 发件人邮箱账号
    my_sender = '1441576268@qq.com'

    # 发件人邮箱密码 密码不是真正的密码是 授权码，授权码是用于登录第三方邮件客户端的专用密码。
    my_pass = 'szlcejiprutxbafa'

    # 收件人邮箱账号
    # my_user = '18569938068@163.com'
    my_user = user_email
    # print("开始填信")
    ret = True
    mail_msg = '<h1>欢迎您</h1>请点击下方链接进行密码找回(30分钟内有效)<br><a href="{0}">点我激活登陆</a>'.format(url)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["圈儿（circle", my_sender])
    msg['To'] = formataddr(["尊敬的", my_user])
    msg['Subject'] = '圈儿（circle）--python 技术社区'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()
    print("end")
    ret = False
    return ret


def follow_email(user_email, str):
    url = "http://www.ofus.ink/users/my_page/"
    # 发件人邮箱账号
    my_sender = '1441576268@qq.com'
    # 发件人邮箱密码 密码不是真正的密码是 授权码，授权码是用于登录第三方邮件客户端的专用密码。
    my_pass = 'szlcejiprutxbafa'
    # 收件人邮箱账号
    # my_user = '18569938068@163.com'
    my_user = user_email
    # print("开始填信")
    ret = True
    mail_msg = '{0}<br><a href="{1}">点我进入查看</a>'.format(str,url)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["圈儿（circle", my_sender])
    msg['To'] = formataddr(["尊敬的", my_user])
    msg['Subject'] = '圈儿（circle）--python 技术社区'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()
    print("end")
    ret = False
    return ret
