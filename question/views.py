from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models


def index(request):
    return render(request, 'question/index.html', {})


@login_required
def add_question(request):
    return render(request, 'question/add_question.html', {})


# def answer(request, q_id):
#     print(q_id)
#     return render(request, 'question/answer.html', {'q_id':q_id})


def answer(request, q_id):
    question = models.Question.objects.get(pk = q_id)
    answer = models.Answer.objects.filter(link_question=question)
    question.browse_num += 1
    question.save()
    print(answer)
    return render(request, 'question/answer.html', {'question':question, 'answer':answer})


def detail(request, answer_id):
    answer = models.Answer.objects.get(pk=answer_id)
    print(answer.link_question)
    question = models.Question.objects.get(pk=answer.link_question_id)
    answer_count = models.Answer.objects.filter(link_question=question).count()
    print(answer_count)
    return render(request, 'question/detail.html', {'answer': answer, 'question': question, 'answer_count':answer_count})