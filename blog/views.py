from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .serializers import MyTokenObtainPairSerializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Article, User
from .serializers import ArticleSerializer
# 使用Generic APIView & Mixins
from rest_framework import mixins
from rest_framework import generics

# generic class-based views
from rest_framework import generics

from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly


# 视图集 viewset
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     ReadOnlyModelViewSet仅提供list和detail可读动作
#     """
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#
# class ArticleViewSet(viewsets.ModelViewSet):
#     # 用一个视图集替代ArticleList和ArticleDetail两个视图
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     # 自行添加，将request.user与author绑定
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# generics类
# generics.ListCreateAPIView类支持List、Create两种视图功能，分别对应GET和POST请求。
class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 将request.user与author绑定
    # 由于ArticleSerializer中author字段仅为可读，需手动关联
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# generics.RetrieveUpdateDestroyAPIView支持Retrieve、Update、Destroy操作，其对应方法分别是GET、PUT和DELETE。
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


# mixin类和GenericAPI的混用
# class ArticleList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ArticleDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#     # perform_create这个钩子函数是CreateModelMixin类自带的，用于执行创建对象时需要执行的其它方法，比如发送邮件等功能，有点类似于Django的信号。
#     # 将request.user与author绑定。调用create方法时执行如下函数。
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# 基础 API 类
# @api_view(['GET', 'POST'])
# # @permission_classes((permissions.AllowAny,))
# def article_list(request, format=None):
#     """
#     List all articles, or create a new article.
#     """
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         # many=True告诉序列化器处理的是多个对象
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             # Very important. Associate request.user with author
#             # 注意：由于序列化器中author是read-only字段，用户是无法通过POST提交来修改的，我们在创建Article实例时需手动将author和request.user绑定
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# # @permission_classes((permissions.AllowAny,))
# def article_detail(request, pk, format=None):
#     """
#     Retrieve，update or delete an article instance。"""
#     try:
#         # pk参数，表示文章的主键（Primary Key），通常是文章的唯一标识符。
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Token
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
