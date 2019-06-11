from django.conf.urls import url
from . import views
from . import api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_question/$', views.add_question, name='add_question'),
    url(r'^answer/(\d+)/$', views.answer, name='answer'),
    url(r'^answer/detail/(\d+)/$', views.detail, name='detail'),

    url(r'^api/v1/add_question/$', api.add_question, name='add_question'),
    url(r'^api/v1/get_types/$', api.get_types, name='get_types'),
    url(r'^api/v1/get_question_answer/$', api.get_question_answer, name='get_question_answer'),
    url(r'^api/v1/get_question_answer_list/$', api.get_question_answer_list, name='get_question_answer_list'),
    url(r'^api/v1/add_answer/$', api.add_answer, name='add_answer'),
    url(r'^api/v1/del_article/$', api.del_article, name='del_article'),
    url(r'^api/v1/del_question/$', api.del_question, name='del_question'),



]