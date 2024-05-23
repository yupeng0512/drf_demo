from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 关系序列化
    # articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # articles = serializers.StringRelatedField(many=True, read_only=True)
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'articles',)
        read_only_fields = ('id', 'username',)


class ArticleSerializer(serializers.ModelSerializer):
    # author不可见并让DRF根据request.user自动补全这个字段
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #  author = serializers.ReadOnlyField(source="author.username")
    author = UserSerializer(read_only=True)  # required=False表示可接受匿名用户，many=True表示有多个用户。
    # 定义了一个仅可读的status字段把原来的status字段覆盖了，这样反序列化时用户将不能再对文章发表状态进行修改（原来的status字段是可读可修改的）。
    # status = serializers.ReadOnlyField(source="get_status_display")
    full_status = serializers.ReadOnlyField(source="get_status_display")
    # SerializerMethodField通常用于显示模型中原本不存在的字段，类似可读字段，你不能通过反序列化对其直接进行修改。
    cn_status = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')

    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''

    def create(self, validated_data):
        """
        Create a new "article" instance
        """
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Use validated data to return an existing `Article`instance。"""
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token