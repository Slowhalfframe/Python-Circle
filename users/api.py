from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout     # 内置的用户认证
from django.db import transaction
from . import models
from django.db.models import Q
from . import user_chenck_email


def ajax_reg(request):
    # 注册
    ret = {'code': 0, 'msg': None, 'data': None}
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    print(email, password, confirm_password)

    # 判断传过来的值合法性
    if len(password) < 6:
        ret['code'] = 1
        ret['msg'] = '密码长度不足6位'
    elif password != confirm_password:
        ret['code'] = 2
        ret['msg'] = '两次输入不同'
    else:
        try:
            User.objects.get(email=email)
            ret['code'] = 3
            ret['msg'] = '邮箱已被注册'
        except:
            try:
                with transaction.atomic():
                    print("开始注册")
                    user = User.objects.create_user(password=password, username=email, email=email)
                    usera = models.User_more_info(u_link_user=user, u_nick_name=email)
                    user.save()
                    usera.save()
                    # 执行登录
                    ret['code'] = 0
                    ret['msg'] = '注册成功'
            except Exception as e:
                ret['code'] = -1
                ret['msg'] = '注册失败'
    return JsonResponse(ret)


def ajax_sign_in(request):
    # 登录
    ret = {'code': 0, 'msg': None, 'data': None}
    email = request.POST['email']
    password = request.POST['password']
    islong = request.POST.get("islong", "")
    next_url = request.POST.get("next", "/")
    print(email, password, islong, next_url)

    # 开始登录
    user = authenticate(username=email, password=password)
    print("结果", user)
    print("session", request.session)

    if user is not None:
        if user.is_active:
            login(request, user)
            # request.session["LoginUser"] = user
            if islong == "on":
                request.session.set_expiry(3600 * 24 * 7)
            else:
                request.session.set_expiry(0)
            ret['msg'] = "登录成功"
    else:
        ret['code'] = -2
        ret['msg'] = "账户、密码错误"
        print("密码错误")
    print("返回结果", ret)
    return JsonResponse(ret)


@login_required
def ajax_change_name(request):
    # 获取修改昵称页面的昵称
    ret = {'code': 0, 'msg': None, 'data': None}
    id = request.POST['u_id']
    print(id)
    obj = models.User_more_info.objects.get(u_link_user = id)
    print("查到了")
    print(obj)
    print(obj.u_nick_name)
    ret['data'] = obj.u_nick_name
    return JsonResponse(ret)


@login_required
def ajax_change_new_name(request):
    # 修改昵称
    ret = {'code': 0, 'msg': None, 'data': None}
    id = request.POST['u_id']
    new_name = request.POST['new_name']
    print(id)
    obj = models.User_more_info.objects.get(u_link_user = id)
    print("查到了")
    obj.u_nick_name = new_name
    obj.save()
    print(obj.u_nick_name)
    ret['data'] = obj.u_nick_name
    ret['msg'] = "修改成功"
    return JsonResponse(ret)


def ajax_change_new_qm(request):
    # 修改昵称
    ret = {'code': 0, 'msg': None, 'data': None}
    id = request.POST['u_id']
    new_qm = request.POST['new_qm']
    print(id)
    obj = models.User_more_info.objects.get(u_link_user = id)
    print("查到了")
    obj.u_autograph = new_qm
    obj.save()
    print(obj.u_autograph)
    ret['data'] = obj.u_autograph
    ret['msg'] = "修改成功"
    return JsonResponse(ret)

'''
修改密码
html页面先出来输入原密码的输入框 
JS把当前用户ID传入后台进行验证
成功：JS生成新密码和确认密码输入框
失败：提示
JS传后台后先验证密码够不够6位，是否两个相等。
再修改密码
提示 修改成功  
推出当前登录 到登录页面

修改头像
暂不着急
'''


@login_required
def ajax_get_email_is(request):
    ret = {'code': 0, 'msg': None, 'data': None}
    id = request.user.id
    obj = models.User_more_info.objects.get(u_link_user = id)
    print(obj.u_check_email)
    ret['data'] = obj.u_check_email
    return JsonResponse(ret)


@login_required
def ajax_send_check_email(request):
    ret = {'code': 0, 'msg': None, 'data': None}
    try:
        id = request.user.id
        obj = User.objects.get(pk=id)
        email = obj.email
        print(email, id, obj)
        from . import user_chenck_email
        res = user_chenck_email.mail(email, id)
        print(res)
        ret['msg'] = "验证邮件发送成功,请前往您的邮箱进行验证"
    except Exception as e:
        ret['code'] = -1
        ret['msg'] = "发送失败"
    return JsonResponse(ret)


def ajax_get_oldpassword(request):
    # 验证旧密码是否正确
    ret = {'code': 0, 'msg': None, 'data': None}
    try:
        id = request.POST['id']
        old_pwd = request.POST['old_password']
        print(id, old_pwd)
        u = User.objects.get(pk = id)
        print(u)
        print(u.username)
        user = authenticate(username=u.username, password=old_pwd)
        print(user)
        if user is None:
            ret['code'] = -1
            ret['msg'] = "输入的旧密码不正确"
        else:
            ret['msg'] = "输入的旧密码正确"
    except Exception as e:
        ret['code'] = -1
        ret['msg'] = "输入的旧密码不正确"

    return JsonResponse(ret)


def ajax_change_password(request):
    # 修改密码
    ret = {'code': 0, 'msg': None, 'data': None}
    id = request.POST['id']
    old_Pwd = request.POST['old_Pwd']
    new_pwd = request.POST['new_pwd']
    confirm_pwd = request.POST['confirm_pwd']
    print(id, new_pwd, confirm_pwd)
    user = User.objects.get(pk = id)
    user = authenticate(username=user.username, password=old_Pwd)
    if user is None:
        ret['code'] = -1
        ret['msg'] = "输入的旧密码不正确"
    else:
        if len(new_pwd) < 6:
            ret['code'] = -2
            ret['msg'] = "新密码长度小于6位"
        elif new_pwd != confirm_pwd:
            ret['code'] = -3
            ret['msg'] = "两次输入密码不一致"
        else:
            user.set_password(new_pwd)
            user.save()
            user_logout(request)
            ret['msg'] = "修改成功，请重新登录账号"
    return JsonResponse(ret)


@login_required
def user_logout(request):
    logout(request)
    return redirect('/users/')


def ajax_get_user_is(request):
    ret = {'code': 0}
    if request.method == 'POST':
        try:
            user_is = request.user
            user_more = models.User_more_info.objects.get(u_link_user=user_is)
            print(user_more.u_nick_name)
            head = str(user_more.u_header)
            ret['user'] = head
        except Exception as e:
            print("未登录", e)
            ret['code'] = -1
    else:
        ret['code'] = -2
    return JsonResponse(ret)

def follow(request):
    ret = {'code':0}
    try:
        user = request.user
        user_more_info = models.User_more_info.objects.get(u_link_user=user)
        follow_user_id = request.POST['user_id']
        to_follow_user = User.objects.get(pk=follow_user_id)
        to_follow_user_more_info = models.User_more_info.objects.get(u_link_user=to_follow_user)
        q = user_more_info.u_nick_name
        w = to_follow_user_more_info.u_nick_name
        if not models.UserFollow.objects.filter(follow=user, fan=to_follow_user).exists():
            print(1)
            follow_user = models.UserFollow(follow=user, fan=to_follow_user)
            follow_user.save()
            print(q, '关注了', w)
            ret['msg'] = '您已成功关注了{0}'.format(w)
            ret['data'] = True
            sss = '{0}关注了您。'.format(q)
            user_chenck_email.follow_email(to_follow_user.email, sss)
        else:
            relationship = models.UserFollow.objects.get(Q(follow=user) & Q(fan=to_follow_user))  # 通过关注者和被关注的信息，查出这个关系实例
            relationship.delete()
            print(q,'已取消关注',w)
            ret['data'] = False
            ret['msg'] = '您已成功取消关注了{0}'.format(w)
    except Exception as e:
        print(e)
        ret['code'] = -3
    return JsonResponse(ret)


# 获取所有我关注的人
def get_all_fan(request):
    ret = {'code':0}
    try:
        user = request.user
        if request.method == 'GET':
            fans = models.UserFollow.objects.filter(follow=user).count()
            ret['data'] = fans
        if request.method == 'POST':
            fans = models.UserFollow.objects.filter(follow=user)
            fans_list = []
            for f in fans:
                name = models.User_more_info.objects.get(u_link_user=f.fan.id)
                user = {
                    'pk': f.fan.id,
                    'name': name.u_nick_name
                }
                fans_list.append(user)
            ret['data'] = fans_list
    except Exception as e:
        print(e)
        ret['code'] = -3
    return JsonResponse(ret)


# 获取所有关注我的人
def get_all_follow(request):
    ret = {'code': 0}
    try:
        user = request.user
        if request.method == 'GET':
            fans = models.UserFollow.objects.filter(fan=user).count()
            ret['data'] = fans
        if request.method == 'POST':
            fans = models.UserFollow.objects.filter(fan=user)
            fans_list = []
            for f in fans:
                name = models.User_more_info.objects.get(u_link_user=f.follow.id)
                u = User.objects.get(pk=name.u_link_user.id)
                print('//' * 9, u, user)
                if not models.UserFollow.objects.filter(follow=user, fan=u).exists():
                    # 我还没关注这个用户
                    print(1)
                    user_info = {
                        'pk': f.follow.id,
                        'name': name.u_nick_name,
                        'is': True
                    }
                    fans_list.append(user_info)
                else:
                    # 我已经关注了者个用户
                    print(2)
                    user_info = {
                        'pk': f.follow.id,
                        'name': name.u_nick_name,
                        'is': False
                    }
                    fans_list.append(user_info)
            ret['data'] = fans_list
    except Exception as e:
        print(e)
        ret['code'] = -3
    print(ret)
    return JsonResponse(ret)