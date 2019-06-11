from django.http import JsonResponse
from . import models
from users.models import User_more_info
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
def get_types(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            input_val = request.POST['type_val']
            print(input_val)
            response = models.Question_Type.objects.filter(Q(name__contains=input_val) | Q(intro__contains=input_val))
            print(response)
            data_list = {}
            for r in response:
                print(r)
                print(r.id)
                print(r.name)
                data_list[r.id ] = r.name
            ret['data'] = data_list
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = "出现意外错误", e
    else:
        ret['code'] = -2
        ret['msg'] = "请求方式错误"
    print(ret)
    return JsonResponse(ret)


@login_required
def add_question(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            type_id = request.POST['type_id']
            title = request.POST['title']
            content = request.POST['content']
            print(type_id, title, content)
            question_type = models.Question_Type.objects.get(pk=type_id)
            user_more_info = User_more_info.objects.get(u_link_user=request.user.id)
            question_details = models.Question(q_title=title, q_miaoshu=content, browse_num=0, q_link_user=request.user, user_more_info=user_more_info, q_type=question_type)
            question_details.save()
            ret['msg'] = "发布问题成功，将跳转至您的问题详情页"
            ret['data'] = question_details.id
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = "出现意外错误", e
    else:
        ret['code'] = -2
        ret['msg'] = "请求方式错误"
    print(ret)
    return JsonResponse(ret)


def get_question_answer(request):
    ret = {'code': 0, 'msg': None}
    print("进来了")
    if request.method == 'POST':
        try:
            # 问题部分
            q_id = request.POST['q_id']
            # print("获取到id", q_id)
            # 获取问题
            # 如果获取不到 提示未找到相关信息
            question = models.Question.objects.get(pk=q_id)
            # print(question)
            # print(question.q_title, question.q_miaoshu, question.user_more_info.u_nick_name, question.user_more_info.u_header)
            # 问题的阅读计数
            # count = models.Question_count.objects.get(question=q_id)
            # count.browse_num += 1
            # count.save()
            question.browse_num += 1
            question.save()

            # 返回去的问题字典
            question_over = {
                'q_title': question.q_title, 'miaoshu': question.q_miaoshu,
                'nickname': question.user_more_info.u_nick_name,
                'browse_num': question.browse_num, 'q_id': q_id,
                'create_time' : question.q_create_time
            }

            # print("问题OK。该回答了")
            # 回答部分
            answers = models.Answer.objects.filter(link_question=question)
            # print(answers)
            #
            answers_over = []

            for a in answers:
                # 回答答案详情
                # print(a.a_content)
                # 回答者昵称
                # print(a.user_more_info.u_nick_name)
                # 回答答案ID
                # print(a.id)
                a_count = models.Answer_count.objects.get(Answer=a)
                # print(a_count)
                answers_over.append({'content': a.a_content, 'nickname': a.user_more_info.u_nick_name, 'a_id': a.id, 'zan_num': a_count.zan_num, 'browse_num': a_count.browse_num})

            # print("list", answers_over)

            ret['data'] = {
                'question': question_over,
                'answer': answers_over,
            }
            # print(ret['data'])
            print(type(ret['data']))
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = "出现意外错误", e
    else:
        ret['code'] = -2
        ret['msg'] = "请求方式错误"
    print(ret)
    return JsonResponse(ret)


@login_required
def add_answer(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            q_id =request.POST['q_id']
            answer = request.POST['answer']
            print(q_id, answer)
            on_question = models.Question.objects.get(pk=q_id)
            print(on_question)
            user_more_info = User_more_info.objects.get(u_link_user=request.user.id)
            print(user_more_info)
            with transaction.atomic():
                answer_details = models.Answer(a_content=answer,  q_link_user=request.user, zan_num=0, browse_num=0, user_more_info=user_more_info, link_question=on_question)
                answer_details.save()
                print("欧克")
                # answer_count = models.Answer_count(zan_num=0, browse_num=0, Answer=answer_details)
                # answer_count.save()
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = "出现意外错误", e
    else:
        ret['code'] = -2
        ret['msg'] = "请求方式错误"
    print(ret)
    return JsonResponse(ret)


# 问答首页 数据的展示
# 默认显示最后一条回答的部分摘要
def get_question_answer_list(request):
    ret = {'code': 0, 'msg': None}
    if request.method == 'POST':
        try:
            questions = models.Question.objects.all()
            for q in questions:
                print(q.q_title)
                print(q.browse_num)
                questions_answer_list = [{'q_id': q.id, 'q_title': q.q_title}]
                answer = models.Answer.objects.filter(link_question=q).order_by('-id')[:1]
                print(answer)
                answer_count = models.Answer.objects.filter(link_question=q).count()
                for a in answer:
                    print(a.a_content)
                    # answer_count = models.Answer_count.objects.get(Answer=a)
                    # print(answer_count.zan_num)
                    # print(answer_count.browse_num)
                    questions_answer_list = [{'q_id': q.id, 'q_title': q.q_title,'answer_content':a.a_content, 'answer_browse':q.browse_num, 'answer_auth':a.user_more_info.u_nick_name, 'a_id':a.id, 'answer_count':answer_count}]
                    # answer_list = [{'answer_content':a.a_content, 'answer_zan':answer_count.zan_num, 'answer_browse':answer_count.browse_num}]
            ret['data'] = {
                'questions_answer_list': questions_answer_list,
                # 'answer_list':answer_list,
            }
        except Exception as e:
            ret['code'] = -1
            ret['msg'] = "出现意外错误", e
    else:
        ret['code'] = -2
        ret['msg'] = "请求方式错误"
    print(ret)
    return JsonResponse(ret)


def del_article(request):
    ret = {'code': 0}
    if request.method == 'POST':
        try:
            a_id = request.POST['id']
            print(a_id)
            answer = models.Answer.objects.get(pk=a_id)
            if request.user == answer.q_link_user:
                print(1)
                answer.delete()
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


def del_question(request):
    ret = {'code': 0}
    if request.method == 'POST':
        try:
            a_id = request.POST['id']
            print(a_id)
            question = models.Question.objects.get(pk=a_id)
            if request.user == question.q_link_user:
                print(1)
                question.delete()
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