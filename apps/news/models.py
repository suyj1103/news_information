from django.db import models
from utils.BaseModel import ModelBase
# Create your models here.

class Tag(ModelBase):
    name  = models.CharField(max_length=64,verbose_name='标签名',help_text='标签名')

    class Meta:
        ordering = ['-update_time','-id']
        db_table = 'tb_tag'
        verbose_name = '新闻标签'

    def __str__(self):
        return self.name


class News(ModelBase):
    title = models.CharField( max_length=150,verbose_name='标题',help_text='标题')
    digest = models.CharField(max_length=200,verbose_name='摘要')
    content = models.TextField(verbose_name='内容')
    clicks = models.IntegerField(default=0, verbose_name='点击量')
    image_url= models.URLField(default="",verbose_name='图片')
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL,null=True) # 允许为空
    author = models.ForeignKey('user.Users',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-update_time','-id']
        db_table = 'tb_news'
        verbose_name = '新闻'

    def __str__(self):
        return self.title


class Comments(ModelBase):
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey('user.Users',on_delete=models.SET_NULL,null=True)
    news = models.ForeignKey('News',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

    def to_data(self):
        comments_dict ={
            'news_id':self.news_id,
            'content_id':self.id,
            'content':self.content,
            'author':self.author.username,
            'upsate_time':self.update_time.strftime('%Y年%m月%d日 %H时%M分'),
            'parent':self.parent.to_data() if self.parent else None,
        }
        return comments_dict



    class Meta:
        ordering = ['-update_time','-id']
        db_table = 'tb_comment'
        verbose_name = '评论'

    def __str__(self):
        return '评论{}'.format(self.id)


class HotNews(ModelBase):
    PRI_CHOICES=[
        (1,'第一级'),
        (2,'第二级'),
        (3,'第三级'),
    ]

    news = models.OneToOneField('news',on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRI_CHOICES,verbose_name='热门新闻优先级')

    class Meta:
        ordering = ['-update_time','-id']
        db_table = 'tb_hot'
        verbose_name = '热门新闻'

    def __str__(self):
        return '热门新闻{}'.format(self.id)


class Banner(ModelBase):
    PRI_CHOICES = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
        (4, '第四级'),
        (5, '第五级'),
        (6, '第六级'),
    ]

    image_url = models.URLField(verbose_name='轮播图url')
    priority = models.IntegerField(choices=PRI_CHOICES,default=6,verbose_name='轮播图优先级')
    news = models.OneToOneField('news',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time','-id']
        db_table = 'tb_banner'
        verbose_name = '轮播图'

    def __str__(self):
        return '轮播图{}'.format(self.id)

