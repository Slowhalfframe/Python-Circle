from django.conf.urls import url
from . import views
from . import api


urlpatterns = [
    url(r'^$', views.sign_in, name='sign_in'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^register/$', views.register, name='register'),
    url(r'^change_nickname/$', views.change_nickname, name='change_nickname'),
    # url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^email_verification/(?P<token>.*)$', views.email_verification, name='email_verification'),
    url(r'^forget_pwd/(?P<token>.*)$', views.forget_pwd, name='forget_pwd'),
    url(r'^user_logout/$', api.user_logout, name='user_logout'),
    url(r'^my_page/$', views.my_page, name='my_page'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'forget_password/', views.forget_password, name='forget_password'),
    url(r'change_forget_pwd/', views.change_forget_pwd, name='change_forget_pwd'),
    url(r'^(.*)/checkemail/$', views.checkemail, name='checkemail'),
    url(r'^user_detail/$', views.user_detail, name='user_detail'),
    url(r'^change_header/$', views.change_header, name='change_header'),


    # api
    # api 注册
    url(r'^api/v1/ajax_reg/$', api.ajax_reg, name='ajax_reg'),
    url(r'^api/v1/ajax_sign_in/$', api.ajax_sign_in, name='ajax_sign_in'),
    url(r'^api/v1/ajax_change_name/$', api.ajax_change_name, name='ajax_change_name'),
    url(r'^api/v1/ajax_change_new_name/$', api.ajax_change_new_name, name='ajax_change_new_name'),
    url(r'^api/v1/ajax_change_new_qm/$', api.ajax_change_new_qm, name='ajax_change_new_qm'),
    url(r'^api/v1/ajax_get_email_is/$', api.ajax_get_email_is, name='ajax_get_email_is'),
    url(r'^api/v1/ajax_send_check_email/$', api.ajax_send_check_email, name='ajax_send_check_email'),
    url(r'^api/v1/ajax_get_oldpassword/$', api.ajax_get_oldpassword, name='ajax_get_oldpassword'),
    url(r'^api/v1/ajax_change_password/$', api.ajax_change_password, name='ajax_change_password'),
    url(r'^api/v1/ajax_get_user_is/$', api.ajax_get_user_is, name='ajax_get_user_is'),
    url(r'^api/v1/follow/$', api.follow, name='follow'),
    url(r'^api/v1/get_all_fan/$', api.get_all_fan, name='get_all_fan'),
    url(r'^api/v1/get_all_follow/$', api.get_all_follow, name='get_all_follow'),
]