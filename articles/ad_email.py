import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(article_auth_email,article_auth_name, article_name, article_id, user_name):
    token = article_id
    url = "http://www.ofus.ink/articles/article/{0}/".format(token)
    # 发件人邮箱账号
    my_sender = '1441576268@qq.com'
    # 发件人邮箱密码 密码不是真正的密码是 授权码，授权码是用于登录第三方邮件客户端的专用密码。
    my_pass = 'szlcejiprutxbafa'
    # 收件人邮箱账号
    # my_user = '18569938068@163.com'
    my_user = article_auth_email
    # print("开始填信")
    ret = True
    mail_msg = '您好：{0}！<br>刚刚 用户 【{1}】收藏了您的文章：<a href={2} >{3}</a>,快点击查看下您的文章被多少收藏了吧'.format(article_auth_name,user_name, url,article_name)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["python圈(Circle) python相关技术社区", my_sender])
    msg['To'] = formataddr(["尊敬的", my_user])
    msg['Subject'] = 'python圈(Circle) python相关技术社区'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()
    print("end")
    ret = False
    return ret


def pl_email(to_name, to_email, from_name, from_content, article_title, token):
    url = "http://www.ofus.ink/articles/article/{0}/".format(token)
    # 发件人邮箱账号
    my_sender = '1441576268@qq.com'
    # 发件人邮箱密码 密码不是真正的密码是 授权码，授权码是用于登录第三方邮件客户端的专用密码。
    my_pass = 'szlcejiprutxbafa'
    # 收件人邮箱账号
    # my_user = '18569938068@163.com'
    my_user = to_email
    # print("开始填信")
    ret = True
    mail_msg = '您好：{0}！<br>刚刚 用户 【{1}】评论了您的文章：<a href={2} >{3}</a><br>评论内容：<b>{4}</b>,<br>快点击回复他吧！'.format(to_name,
                                                                                             from_name, url,
                                                                                             article_title, from_content)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['From'] = formataddr(["python圈(Circle) python相关技术社区", my_sender])
    msg['To'] = formataddr(["尊敬的", my_user])
    msg['Subject'] = 'python圈(Circle) python相关技术社区'
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()
    print("end")
    ret = False
    return ret


