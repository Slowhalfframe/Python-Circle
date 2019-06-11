from django.conf.urls import url
from . import views, api

urlpatterns = [
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^article/(\d+)/$', views.article, name='article'),
    url(r'^show_article_type/(\d+)/$', views.show_article_type, name='show_article_type'),
    url(r'^update_article/$', views.updata_article, name='updata_article'),

    url(r'^api/v1/get_two_types/$', api.get_two_types, name='get_two_types'),
    url(r'^api/v1/add_article/$', api.add_article, name='add_article'),
    url(r'^api/v1/zan_add/$', api.zan_add, name='zan_add'),
    url(r'^api/v1/del_article/$', api.del_article, name='del_article'),
    url(r'^api/v1/add_pl/$', api.add_pl, name='add_pl'),
    url(r'^api/v1/add_plhf/$', api.add_plhf, name='add_plhf'),
    url(r'^api/v1/get_pl/$', api.get_pl, name='get_pl'),
    url(r'^api/v1/get_article_type/$', api.get_article_type, name='get_article_type'),
    url(r'^api/v1/get_same_type/$', api.get_same_type, name='get_same_type'),
    url(r'^api/v1/update_article/$', api.update_article, name='update_article'),
    url(r'^api/v1/favorites_articles/$', api.favorites_articles, name='favorites_articles'),
    url(r'^api/v1/off_favorites_articles/$', api.off_favorites_articles, name='off_favorites_articles'),

    # markdown
    url(r'^markdown/$', views.markdown, name='markdown'),
    # markdown api
    url(r'^markdown_api/$', views.MarkdownApi.as_view())

]