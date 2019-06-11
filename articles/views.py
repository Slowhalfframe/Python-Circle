from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import models
from .models import Article_type
from users.models import User_more_info
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import serializers # rf serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator


class ArticleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article_type
        fields = '__all__'

def check_active(func):
    def _check_email(request):
        user = request.user
        user_more_info = User_more_info.objects.get(u_link_user=user)
        if user_more_info.u_check_email == 0:
            print("你的邮箱还未验证")
            return render(request, 'users/setting.html', {})
        else:
            print("请继续操作")
            # 这里怎么写让调用的函数返回
            return func(request)
    return _check_email


@login_required
@check_active
def add_article(request):
    articletypes = models.Article_type.objects.filter(parent_id__isnull=True)
    return render(request, 'articles/add_article.html', {"type1": articletypes})


def article(request, id):
    try:
        article = models.Article.objects.get(pk=id)
        article.count += 1
        article.save()
        # 多个条件查询  并 的关系 既符合是这篇文章的评论 还是 没有关联的评论
        # pl = models.Article_pinglun.objects.filter(Q(article=article) and Q(pinglun_parent=None ))
        pl = models.Article_pinglun.objects.filter(article=article)
        # 可以借鉴翻译系统 将两个列表合并一个列表 zip  最后输出
        # for p in pl:
        #     print(p.content)
        #     print("===")
        #     hf = models.Article_pinglun.objects.filter(Q(article=article) and Q(pinglun_parent=p.id))
        #     print(hf)
            # for h in hf:
            #     print(h.content)
        try:
            f_a = models.Favorites.objects.get(Q(user=request.user) & Q(favorites_articles=article))
            print(f_a)
            is_f_a = True
        except Exception as e:
            print(e)
            is_f_a = False
        favortes_count = models.Favorites.objects.filter(favorites_articles=article).count()
        hot_article_num = models.Article.objects.all().order_by("-count")[:5]
        return render(request, 'articles/article.html', {'article': article, 'pl':pl, 'is_f_a':is_f_a, 'favortes_count':favortes_count,
                                                         'hot_article_num':hot_article_num})
    except:
        return HttpResponse("文章没找到")


def show_article_type(request, type_id):
    type = models.Article_type.objects.get(pk=type_id)
    if type.parent != None:
        articles = models.Article.objects.filter(article_type=type_id).order_by('-create_time')
    else:
        articles = models.Article.objects.filter(article_type__parent_id=type_id).order_by('-create_time')
    pageNow = int(request.GET.get("pageNow", 1))  # 当前的页面
    pageSize = int(request.GET.get("pageSize", 11))  # 一页显示几个
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)
    return render(request, 'articles/types.html', {"pageSize": pageSize, "page": page, 'articles': articles, 'type_id':type_id})


# markdown url
@login_required
def markdown(request):
    return render(request, 'articles/article_markdown.html')

# markdown api
@method_decorator(login_required, name='dispatch')
class MarkdownApi(APIView):
    # 一二级分类
    def get(self, request):
        # article_type = models.Article_type.objects.all()
        # s = ArticleTypeSerializer(instance=article_type, many=True)
        # print(s.data)
        # return JsonResponse(data=s.data, safe=False)
        # 一级分类
        article_type = models.Article_type.objects.filter(parent_id__isnull=True)

        # 定义字典返回自己需要格式化的数据
        data = {}

        # {'python': [], '前端': [], '数据库': [], 'other': [], 'linux': []}
        for i in article_type:
            data[str(i)] = []

        # 二级分类
        article_type = models.Article_type.objects.filter(parent_id__isnull=False)

        # {'other': ['测试用的'], 'python': ['web', '爬虫'], 'linux': ['Ubuntu'], '数据库': ['MySql'], '前端': ['html+css', 'javascript']}
        for i in article_type:
            data[str(i.parent)].append(i.name)
        # 返回一二级分类
        return JsonResponse(data=data, safe=False)


# @login_required
@check_active
def updata_article(request):
    '''
    :param request: 先验证这篇文章的作者 == 当前登录的用户
    :return:     TRUE 返回渲染页面
                 False 返回404
    '''
    article_id = request.GET['article_id']
    article = models.Article.objects.get(pk=article_id)
    if article.user == request.user:
        type1 = models.Article_type.objects.filter(parent=None)
        type2 = models.Article_type.objects.filter(id=article.article_type_id)
        return render(request, 'articles/update_article.html', {'article':article, 'type1':type1, 'type2':type2})
    else:
        print(2)
        return HttpResponse("404")
