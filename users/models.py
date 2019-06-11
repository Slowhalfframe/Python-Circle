from django.db import models
from django.contrib.auth.models import User


class User_more_info(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_header = models.ImageField(upload_to="static/users/header", default='static/users/header/default.png', verbose_name="用户头像")
    u_autograph = models.CharField(max_length=256, verbose_name="个性签名")
    u_nick_name = models.CharField(max_length=123, default="", verbose_name="昵称")
    u_check_email = models.IntegerField(default=0, verbose_name="验证邮箱")
    u_link_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="关联用户")

    def __str__(self):
        return self.u_nick_name

    
class UserFollow(models.Model):
    id = models.AutoField(primary_key=True)
    follow = models.ForeignKey(User, default='', related_name="follow_user", verbose_name="我关注的人")
    fan = models.ForeignKey(User, default='', related_name="fan_user", verbose_name="关注我的人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return '{0}关联{1}'.format(self.follow, self.fan)