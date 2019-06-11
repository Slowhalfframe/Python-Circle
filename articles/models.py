from django.db import models
from django.contrib.auth.models import User
from users.models import User_more_info
from DjangoUeditor.models import UEditorField


# content = models.TextField()



class Article_type(models.Model):
    id = models.AutoField(primary_key=True)
    # 分类名称
    name = models.CharField(max_length=150, unique=True, verbose_name="文章类别名称")
    # 分类的图片
    cover = models.ImageField(upload_to='static/articles/type_cover', default="/static/type_cover/default.jpg", verbose_name="文章类配图")
    # 分类的描述
    intro = models.TextField(verbose_name="文章类别描述")
    # 父级类型
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父级类型", on_delete=models.CASCADE)

    def __str__(self):  # ____unicode____ on Python 2
        return self.name


class Article(models.Model):
    FROM_CHOICES = (
        ('yuanchuang', '原创'),
        ('zhuanzai', '转载'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=66, null=False, verbose_name="文章标题")
    content = UEditorField()
    zhaiyao = models.CharField(max_length=520, verbose_name="文章摘要")
    cover_img = models.ImageField(upload_to="static/articles/cover", verbose_name="文章封面图")
    biaoqian = models.CharField(max_length=256, verbose_name="文章标签")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    article_from = models.CharField(max_length=16, choices=FROM_CHOICES, default='yuanchuang')
    article_type = models.ForeignKey(Article_type, on_delete=models.CASCADE, verbose_name="文章分类")
    count = models.IntegerField(default=0, verbose_name="阅读量")
    zan_num = models.IntegerField(default=0, verbose_name="点赞量")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    user_more_info = models.ForeignKey(User_more_info, on_delete=models.CASCADE, verbose_name="关联用户更多信息")

    def __str__(self):
        return self.title


class Article_zan_log(models.Model):
    id = models.AutoField(primary_key=True)
    link_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    link_article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="关联文章")

    def __str__(self):
        return '{0}点赞了文章：{1}'.format(self.link_user, self.link_article)
# class Article_Count(models.Model):
#     id = models.AutoField(primary_key=True)
#     count = models.IntegerField(default=0, verbose_name="阅读量")
#     link_article = models.OneToOneField(Article, on_delete=models.CASCADE)


class Article_pinglun(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 关联文章
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="关联文章")
    # 关联用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    user_more_info = models.ForeignKey(User_more_info, on_delete=models.CASCADE, verbose_name="关联用户更多信息")
    # 评论自关联 为评论的回复1
    pinglun_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="评论自关联父级")


class Favorites(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorites_articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}收藏了文章：{1}'.format(self.user, self.favorites_articles)


