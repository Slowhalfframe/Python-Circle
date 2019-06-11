from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from . import models
from users.models import User_more_info
import re
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from users.models import User_more_info
from . import ad_email
import json
import random


def api_check_active(func):
    def _check_email(request):
        user = request.user
        user_more_info = User_more_info.objects.get(u_link_user=user)
        if user_more_info.u_check_email == 0:
            ret = {'code': -99, 'data': '/users/user_setting'}
            print("你的邮箱还未验证")
            return JsonResponse(ret)
        else:
            print("请继续操作")
            # 这里怎么写让调用的函数返回
            return func(request)
    return _check_email


def clear_html(content):
    s_content = re.sub(r"</?(.+?)>", "", content)
    print(s_content)
    return s_content


@login_required
def get_two_types(request):
    # ret = {'code': 0, 'msg': None, 'data':None}
    parent_id = request.POST["parent_id"]
    print(parent_id)
    type2 = models.Article_type.objects.filter(parent_id=parent_id)
    print(type2)
    for t in type2:
        print(t.name)
    # ret['msg'] = '二级分类'
    return HttpResponse(serialize("json", type2))


@login_required
@api_check_active
def add_article(request):
    ret = {'code': 0, 'msg': None, 'data': None}
    try:
        id = request.POST.get('u_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        zhaiyao = request.POST.get('zhaiyao')
        type2 = request.POST.get('type2')
        # cover_img = request.POST['cover_img']
        cover_img = request.FILES.get('cover_img')
        editor_from = request.POST.get('editor_from')
        article_type = models.Article_type.objects.get(pk=type2)
        user_more_info = User_more_info.objects.get(u_link_user = request.user.id)
        print(user_more_info)
        print(user_more_info.u_id, user_more_info.u_nick_name)
        print(article_type)
        print(id, title, content, zhaiyao, type2, cover_img)
        print(editor_from)
        print(type(editor_from))
        if editor_from == '1':
            editor_from = "yuanchuang"
        elif editor_from == '2':
            editor_from = 'zhuanzai'
        else:
            editor_from = 'other'
        print("//"*9)
        print(editor_from)
        print("//"*9)
        if len(zhaiyao) < 1:
            print("a")
            zhaiyao = clear_html(content)
            zhaiyao = zhaiyao[:80]
            print("========")
            print(zhaiyao)
            print("==============")
        try:
            cover_img = request.FILES["cover_img"]
            article = models.Article(title=title, content=content, zhaiyao=zhaiyao, article_from=editor_from, article_type=article_type, user=request.user, user_more_info=user_more_info, cover_img=cover_img)
        except:
            article = models.Article(title=title, content=content, zhaiyao=zhaiyao, article_from=editor_from, article_type=article_type, user=request.user, user_more_info=user_more_info)
        article.save()
        ret['msg'] = '发布文章成功'
        ret['data'] = article.id
        # 向所有粉丝发送通知

    except Exception as e:
        ret['code'] = -1
        ret['msg'] = '发布文章失败'
    return JsonResponse(ret)


@login_required
@api_check_active
def zan_add(request):
    print("来赞了")
    ret = {'code': 0}
    if request.method == 'POST':
        try:
            article_id = request.POST['article_id']
            try:
                zan_log = models.Article_zan_log.objects.get(Q(link_user=request.user) & Q(link_article_id=article_id))
                print(zan_log)
                print(zan_log.id)
                ret['code'] = -3
                ret['msg'] = '已经赞过啦'
            except:
                with transaction.atomic():
                    article = models.Article.objects.get(pk = article_id)
                    article.zan_num += 1
                    zan_log = models.Article_zan_log(link_user=request.user, link_article=article)
                    article.save()
                    zan_log.save()
                    ret['data'] = article.zan_num
        except Exception as e:
            ret['code'] = -2
            ret['msg'] = '出现异常', e
    else:
        ret['code'] = -1
        ret['msg'] = '请求方式出错'
    print(ret)
    return JsonResponse(ret)


@login_required
@api_check_active
def del_article(request):
    ret = {'code': 0}
    if request.method == 'POST':
        try:
            a_id = request.POST['id']
            print(a_id)
            article = models.Article.objects.get(pk=a_id)
            if request.user == article.user:
                print(1)
                article.delete()
                ret['msg'] = '删除成功'
            else:
                ret['code'] = -4
                ret['msg'] = '非法访问'
        except Exception as e:
            ret['code'] = -2
            ret['msg'] = '出现异常'
            print(e)
    else:
        ret['code'] = -1
        ret['msg'] = '请求方式出错'
    print(ret)
    return JsonResponse(ret)


@login_required
@api_check_active
def add_pl(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            article_id = request.POST['article_id']
            pl_content = request.POST['pl_content']
            user = request.user
            print(article_id, pl_content, user)
            article = models.Article.objects.get(pk=article_id)
            user_more_info = User_more_info.objects.get(u_link_user=user.id)
            pinglun = models.Article_pinglun(content=pl_content, article=article, user=user, user_more_info=user_more_info)
            pinglun.save()
            header = pinglun.user_more_info.u_header
            header = str(header)
            print(type(header))
            nickname = pinglun.user_more_info.u_nick_name
            print(header)
            ret['code'] = 0
            ret['msg'] = '评论成功'
            ret['data'] = {
                'header': header,
                'nickname': nickname,
                'content': pinglun.content,
            }
            # 收件人邮箱         article.user.email
            # 收件人昵称         article.user_more_info.u_nick_name
            # 评论的昵称          from_user = user_more_info.u_nick_name
            # 评论的内容          pl_content
            # 评论文章名          article.title
            ad_email.pl_email(article.user_more_info.u_nick_name, article.user.email, user_more_info.u_nick_name, pl_content, article.title, article.id)
        except Exception as e:
            ret['code'] = 1
            print("**", e)
            ret['msg'] = '出现异常' + str(e)
    else:
        ret['code'] = -1
        ret['msg'] = '请求方式出错'
    return JsonResponse(ret, safe=False)


@login_required
@api_check_active
def add_plhf(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            article_id = request.POST['article_id']
            pl_content = request.POST['pl_neirong']
            pl_parent = request.POST['pl_id']
            user = request.user
            print(article_id, pl_content, user, pl_parent)
            article = models.Article.objects.get(pk=article_id)
            user_more_info = User_more_info.objects.get(u_link_user=user.id)
            parent_pl = models.Article_pinglun.objects.get(pk=pl_parent)
            pinglun = models.Article_pinglun(content=pl_content, article=article, user=user,
                                             user_more_info=user_more_info, pinglun_parent=parent_pl)
            pinglun.save()
            header = pinglun.user_more_info.u_header
            header = str(header)
            print(type(header))
            nickname = pinglun.user_more_info.u_nick_name
            print(header)
            ret['code'] = 0
            ret['msg'] = '回复成功'
            ret['data'] = {
                'pk': pinglun.id,
                'header': header,
                'nickname': nickname,
                'content': pinglun.content,
                'create_time': pinglun.create_time
            }
        except Exception as e:
            ret['code'] = 1
            print("**", e)
            ret['msg'] = '出现异常' + str(e)
    else:
        ret['code'] = -1
        ret['msg'] = '请求方式出错'
    return JsonResponse(ret, safe=False)


def get_pl(request):
    id = request.GET.get('id')
    pls = list(models.Article_pinglun.objects.filter(article_id=id).values('pk', 'content', 'create_time', 'pinglun_parent', 'user__user_more_info__u_nick_name', 'user__user_more_info__u_header'))
    # pl_list = []
    # for pl in pls:
    #     print(pl.pk)
    #     print(pl.content)
    # print(pls)
    return JsonResponse(pls, safe=False)
    # for pl in pls:
    #     print(pl)
    #     print(pl.id)
    #     print(pl.content)
    #     hfpl = models.Article_pinglun.objects.filter(Q(article_id=id) & Q(pinglun_parent_id=pl.id))
    #     for h in hfpl:
    #         print("回复评论", h.content)


def get_article_type(request):
    ret = {'code': 0}
    article_type = models.Article_type.objects.all().values('name', 'id')
    print(article_type)
    types = []
    for type in article_type:
        print(type)
        types.append(type)
    ret['data'] = types
    return JsonResponse(ret)


def get_same_type(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'GET':
        try:
            type_id = request.GET['type_id']
            same_article = models.Article.objects.filter(article_type_id=type_id).order_by('count')
            if len(same_article) - 6 > 1:
                index = random.randint(0, len(same_article) - 6)
                print(index)
            else:
                index = 0
            same_article = same_article[index:6 + index]
            data = []
            for sa in same_article:
                a = {
                    'pk':sa.id,
                    'name':sa.title,
                }
                data.append(a)
                ret['data'] = data
        except Exception as e:
            ret['code'] = 1
            print("**", e)
            ret['msg'] = '出现异常' + str(e)
    else:
        ret['code'] = -1
        ret['msg'] = '请求方式出错'
    return JsonResponse(ret, safe=False)


def update_article(request):
    ret = {'code': 0, 'msg': None, 'data': None}
    try:
        id = request.POST.get('u_id')
        article_id = request.POST.get('article_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        zhaiyao = request.POST.get('zhaiyao')
        type2 = request.POST.get('type2')
        cover_img = request.FILES.get('cover_img')
        editor_from = request.POST.get('editor_from')
        article_type = models.Article_type.objects.get(pk=type2)
        user_more_info = User_more_info.objects.get(u_link_user=request.user.id)
        if editor_from == '1':
            editor_from = "yuanchuang"
        elif editor_from == '2':
            editor_from = 'zhuanzai'
        else:
            editor_from = 'other'
        if len(zhaiyao) < 1:
            zhaiyao = clear_html(content)
            zhaiyao = zhaiyao[:80]
        article =models.Article.objects.get(pk=article_id)
        try:
            with transaction.atomic():
                cover_img = request.FILES["cover_img"]
                article.title = title
                article.content = content
                article.zhaiyao = zhaiyao
                article.article_from = editor_from
                article.article_type = article_type
                article.user = request.user
                article.user_more_info = user_more_info
                article.cover_img = cover_img
                article.save()
        except:
            with transaction.atomic():
                article.title = title
                article.content = content
                article.zhaiyao = zhaiyao
                article.article_from = editor_from
                article.article_type = article_type
                article.user = request.user
                article.user_more_info = user_more_info
                article.save()
        ret['msg'] = '修改文章成功'
        ret['data'] = article.id
    except Exception as e:
        ret['code'] = -1
        ret['msg'] = '修改文章失败', e
    return JsonResponse(ret)


def favorites_articles(request):
    res = {'code': 0}
    try:
        article_id = request.POST['article_id']
        user = request.user
        article = models.Article.objects.get(pk=article_id)
        try:
            zan_log = models.Favorites.objects.get(Q(user=user) & Q(favorites_articles=article))
            print(zan_log, '*'*9)
            res['code'] = -2
        except Exception as e:
            print(e)
            f_a = models.Favorites(user=user, favorites_articles=article)
            # 发送通知邮件
            # 谁 收藏了你的 哪一篇文章 文章链接  文章作者
            user_more_info = User_more_info.objects.get(u_link_user=user)
            user_name = user_more_info.u_nick_name
            article_name = article.title
            article_id = article.id
            article_auth_email = article.user.email
            article_auth_name = article.user_more_info.u_nick_name
            ret = ad_email.mail(article_auth_email, article_auth_name, article_name, article_id, user_name)
            f_a.save()
            favorites_count = models.Favorites.objects.filter(favorites_articles=article).count()
            res['data'] = favorites_count
    except Exception as e:
        res['code'] = -3
        print(e)
    return JsonResponse(res)


def off_favorites_articles(request):
    res = {'code': 0}
    try:
        article_id = request.POST['article_id']
        user = request.user
        article = models.Article.objects.get(pk=article_id)
        try:
            zan_log = models.Favorites.objects.get(Q(user=user) & Q(favorites_articles=article))
            zan_log.delete()
            favorites_count = models.Favorites.objects.filter(favorites_articles=article).count()
            res['data'] = favorites_count
        except Exception as e:
            print(e)
            res['code'] = -2
    except Exception as e:
        res['code'] = -3
        print(e)
    return JsonResponse(res)
