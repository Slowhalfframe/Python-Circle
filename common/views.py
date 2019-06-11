from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from articles import models
from django.core.paginator import Paginator
import math
from django.db.models import Count
from django.contrib.auth.models import User


def index(request):
    articles = models.Article.objects.all().order_by('-create_time')
    # print(articles)
    pageNow = int(request.GET.get("pageNow", 1))  # 当前的页面
    pageSize = int(request.GET.get("pageSize", 11))  # 一页显示几个
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)
    type_list = models.Article_type.objects.filter(parent=None)
    # 获取当前所有文章数量
    article_num = models.Article.objects.all().count()
    # 获取当前所有用户数量
    user_num = User.objects.all().count()
    # 前五活跃用户
    hot_user = User.objects.all().order_by('-last_login')[:5]
    return render(request, 'common/index.html',
                  {"pageSize": pageSize, "page": page, "articles": articles, 'type_list': type_list,
                   'article_num': article_num, 'user_num': user_num, 'hot_user': hot_user})


def load_articles(request):
    articles = models.Article.objects.all().order_by('-create_time')  # 查询所有数据
    pageNow = int(request.GET.get("pageNow", 1))  # 当前是第几页
    pageSize = int(request.GET.get("pageSize", 1))   # 一页显示几个
    allCount = len(articles)        # 当前共有多少篇文章
    pageCount = math.ceil(allCount/pageSize)     # 所以文章数量/一页显示几个  向上取整 得到一共有多少页
    page = articles[(pageNow - 1) * pageSize:pageNow * pageSize]   # 从第几个开始取，取几个
    # pagerange = range(1, pageCount+1)     # 构造循环器
    data = serialize('json', page)
    return JsonResponse({"msg": data, "success": True})


# def sitemap(request):
#     return render(request, 'common/sitemap.xml', {})

def get_chrild_type(request):
    ret = {'code':0}
    try:
        if request.method == 'GET':
            type_id = request.GET['type_id']
            # chrild = models.Article_type.objects.filter(parent_id=type_id)
            chrild = models.Article_type.objects.filter(parent_id=type_id).annotate(c=Count("article")).values('name', 'id', 'c')
            print(chrild)
            data = []
            for c in chrild:
                data.append(c)
            ret['data'] = data
        else:
            ret['code'] = -2
            ret['msg'] = "访问方式出错"
    except Exception as e:
        print(e)
        ret['code'] = -1
        ret['msg'] = "出现异常", e
    return JsonResponse(ret)
