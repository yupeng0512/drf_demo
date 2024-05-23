from django.template.defaulttags import url
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'articles', viewset=views.ArticleViewSet)

# article_list = views.ArticleViewSet.as_view(
#     {
#         'get': 'list',
#         'post': 'create'
#     })
#
# article_detail = views.ArticleViewSet.as_view({
#     'get': 'retrieve',  # 只处理get请求，获取单个记录
# })

urlpatterns = [
    # re_path(r'^articles/$', article_list, name='article-list'),
    # re_path(r'^articles/(?P<pk>[0-9]+)/$', article_detail, name='article-detail'),
    re_path(r'^articles/$', views.ArticleList.as_view(), name='article-list'),
    re_path(r'^articles/(?P<pk>[0-9]+)$', views.ArticleDetail.as_view(), name='article-detail'),
]

# urlpatterns += [
#     url(r'^api-token-auth/', views.CustomAuthToken.as_view())]

# 可选：为这些 URL 配置添加格式后缀
urlpatterns = format_suffix_patterns(urlpatterns)
