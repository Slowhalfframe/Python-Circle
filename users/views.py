from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from itsdangerous import TimedJSONWebSignatureSerializer
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib.auth.models import User
from . import user_chenck_email
from django.db.models import Q
# 文章和问答models
from articles.models import Article
from question.models import Question, Answer


@require_http_methods('GET')
def sign_in(request):
    # 显示登录界面
    try:
        next_url = request.GET['next']
    except:
        next_url = "/"

    print(next_url)
    return render(request, 'users/sign_in.html', {"next_url": next_url})
    # return render(request, 'users/sign_in.html', {})


@require_http_methods('GET')
def register(request):
    # 显示注册界面
    return render(request, 'users/register.html', {})


@login_required
def change_nickname(request):
    # 修改昵称
    return render(request, 'users/change_nickname.html', {})


@login_required
def change_password(request):
    # 修改密码
    return render(request, 'users/change_password.html', {})


def email_verification(request, token):
    SECRET_KEY = '3_&qbax4_(xf!%ahsbahn(*8%o2-_1rzm)zr@^nht8q-dwq09z'
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600*24)
    try:
        data = s.loads(token)
        id = data["confirm"]
        print(id)
        user = models.User_more_info.objects.get(u_link_user=id)
        user.u_check_email = 1
        user.save()
        return redirect('/')
    # 验证失败，会抛出异常
    except:
        print("over")
        return HttpResponse('激活链接已过期')


@login_required
def my_page(request):
    user = request.user
    user_more_info = models.User_more_info.objects.get(u_link_user_id=request.user.id)
    # 文章，提问，回答总数量
    article_count = Article.objects.filter(user=request.user).count()
    question_count = Question.objects.filter(q_link_user=request.user).count()
    answer_count = Answer.objects.filter(q_link_user=request.user).count()
    favorites_articles_count = request.user.favorites_set.all().count()
    # 文章，提问，回答
    articles = Article.objects.filter(user=request.user).order_by('-create_time')
    question = Question.objects.filter(q_link_user=request.user)
    answer = Answer.objects.filter(q_link_user=request.user)
    favorites_articles = request.user.favorites_set.all()
    # 关注人数：
    follow_count = models.UserFollow.objects.filter(follow=user).count()
    # 粉丝人数：
    fan_count = models.UserFollow.objects.filter(fan=user).count()
    ret = {"user_more_info": user_more_info, 'article_count': article_count,
           'question_count': question_count, 'answer_count': answer_count,
           'favorites_articles_count': favorites_articles_count, 'articles': articles,
           'question': question, 'answer': answer, 'favorites_articles': favorites_articles,
           'follow_count': follow_count, 'fan_count': fan_count,
           }
    return render(request, 'users/mypage.html', ret)


@login_required
def edit(request):
    user_more_info = models.User_more_info.objects.get(u_link_user_id=request.user.id)
    return render(request, 'users/edit.html', {'user_more_info': user_more_info})


@login_required
def setting(request):
    return render(request, 'users/setting.html', {})


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'users/forget_password.html', {})
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        user = User.objects.get(email=email)
        print(user)
        print(user.id)
        user_chenck_email.forget_email(email, user.id)
        return JsonResponse({'code': 0})


# 找回密码
def forget_pwd(request, token):
    SECRET_KEY = 's(do(h$i-d3rzrx7yhw@ik!cgwg+52-c#roc*3gk#wfk2y@1=2'
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600 * 0.5)
    try:
        data = s.loads(token)
        id = data["confirm"]
        print(id)
        return render(request, 'users/forget_pwd.html', {'id': id})
    except:
        print("over")
        return HttpResponse('激活链接已过期')


# 获取邮箱和修改找回密码
def change_forget_pwd(request):
    ret = {'code': 0}
    if request.method == 'GET':
        try:
            id = request.GET['id']
            user = User.objects.get(pk=id)
            user_info = models.User_more_info.objects.get(u_link_user=user)
            username = user_info.u_nick_name
            ret['data'] = {
                'username': username,
                'email': user.email,
            }
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = e
        return JsonResponse(ret)

    if request.method == 'POST':
        try:
            new_pwd = request.POST['password']
            id = request.POST['id']
            user = User.objects.get(pk=id)
            user.set_password(new_pwd)
            user.save()
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = e
        return JsonResponse(ret)


# ajax验证邮箱
def checkemail(request, email):
    try:
        User.objects.get(email=email)
        return JsonResponse({"msg": "此邮箱已注册，请重新输入", "success": False})
    except:
        return JsonResponse({"msg": "邮箱可用，请继续输入", "success": True})


def user_detail(request):
    try:
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user_more_info = models.User_more_info.objects.get(u_link_user_id=id)
        # 文章，提问，回答总数量
        article_count = Article.objects.filter(user=user).count()
        question_count = Question.objects.filter(q_link_user=user).count()
        answer_count = Answer.objects.filter(q_link_user=user).count()
        favorites_articles_count = user.favorites_set.all().count()
        # 文章，提问，回答
        articles = Article.objects.filter(user=user).order_by('count')
        question = Question.objects.filter(q_link_user=user)
        answer = Answer.objects.filter(q_link_user=user)
        favorites_articles = user.favorites_set.all()
        # 关注人数：
        follow_count = models.UserFollow.objects.filter(follow=user).count()
        # 粉丝人数：
        fan_count = models.UserFollow.objects.filter(fan=user).count()
        # 获取登录用户是否已经关注了当前用户
        try:
            f_a = models.UserFollow.objects.get(Q(follow=request.user) & Q(fan=user))
            print(f_a)
            is_f_a = False
        except Exception as e:
            print(e)
            is_f_a = True
        ret = {"user_more_info": user_more_info, 'article_count': article_count, 'question_count': question_count,
               'answer_count': answer_count, 'articles': articles, 'question': question, 'answer': answer,
               'favorites_articles_count': favorites_articles_count, 'favorites_articles': favorites_articles,
               'is_f_a': is_f_a, 'follow_count':follow_count, 'fan_count':fan_count}
        return render(request, 'users/user_detail.html', ret)
    except:
        return HttpResponse(404)


def change_header(request):
    file = request.FILES['header']
    id = request.POST['user']
    print(file, id)
    user_info = models.User_more_info.objects.get(pk=id)
    user_info.u_header = file
    user_info.save()
    return redirect('/users/edit/')