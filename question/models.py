from django.db import models
from django.contrib.auth.models import User
from users.models import User_more_info
from DjangoUeditor.models import UEditorField


class Question_Type(models.Model):
    id = models.AutoField(primary_key=True)
    # 分类名称
    name = models.CharField(max_length=150, unique=True, verbose_name="问题类别名称")
    # 分类的图片
    cover = models.ImageField(upload_to='static/question/type_cover', default="/static/type_cover/default.jpg", verbose_name="问题类配图")
    # 分类的描述
    intro = models.TextField(verbose_name="问题类别描述")


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    q_title = models.CharField(max_length=256, verbose_name="问题标题")
    q_miaoshu = models.TextField(verbose_name="问题描述")
    q_type = models.ForeignKey(Question_Type, on_delete=models.CASCADE, verbose_name="问题分类")
    browse_num = models.IntegerField(default=0, verbose_name="被浏览量")
    q_create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    q_change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    q_link_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    user_more_info = models.ForeignKey(User_more_info, on_delete=models.CASCADE, verbose_name="关联用户更多信息")
    # browse_count = models.OneToOneField(Question_count, on_delete=models.CASCADE, verbose_name="浏览量")


# class Question_count(models.Model):
#     id = models.AutoField(primary_key=True)
#     browse_num = models.IntegerField(default=0, verbose_name="被浏览量")
#     question = models.OneToOneField(Question, models.CASCADE, verbose_name="关联问题")


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    a_content = models.TextField(verbose_name="回答详情")
    # a_content = UEditorField()
    q_create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    q_change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    zan_num = models.IntegerField(default=0, verbose_name="点赞量")
    browse_num = models.IntegerField(default=0, verbose_name="被浏览量")
    q_link_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    user_more_info = models.ForeignKey(User_more_info, on_delete=models.CASCADE, verbose_name="关联用户更多信息")
    link_question = models.ForeignKey(Question, default="", on_delete=models.CASCADE, verbose_name="关联问题")


# class Answer_count(models.Model):
#     id = models.AutoField(primary_key=True)
#     zan_num = models.IntegerField(default=0, verbose_name="点赞量")
#     browse_num = models.IntegerField(default=0, verbose_name="被浏览量")
#     Answer = models.OneToOneField(Answer, models.CASCADE, verbose_name="关联回答")
