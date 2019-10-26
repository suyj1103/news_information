from django.db import models


class ModelBase(models.Model):
    """
    创建时间
    更新时间
    逻辑删除
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    class Meta:
        # 指定抽象类，数据库迁移不会创建表
        abstract = True


