from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(models.Model):
    """Article Model"""
    # 这是一个包含元组的列表，每个元组定义了文章状态的一个可能值。这里定义了两个状态：'p' 代表已发布（Published），'d' 代表草稿（Draft）。这些状态将在模型字段中以选择的形式展示。
    STATUS_CHOICES = (
        ('p', _('Published')),
        ('d', _('Draft')),
    )

    # verbose_name参数为该字段在Django管理界面中显示的名称。
    title = models.CharField(verbose_name=_('Title (*)'), max_length=90, db_index=True)
    body = models.TextField(verbose_name=_('Body'), blank=True)
    # 多对一关系
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(_('Status (*)'), max_length=1, choices=STATUS_CHOICES, default='d', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # 在查询文章列表时默认按照创建时间的降序排列
        ordering = ['-create_date']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
