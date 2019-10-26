from django.db.models import F
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from . import models
# Create your views here.
from django.http import HttpResponse,HttpResponseNotFound
import logging
logger = logging.getLogger('django')
from utils.res_code import to_json_data,Code,error_map
import json

def index(request):
    tags = models.Tag.objects.only('name','id').filter(is_delete=False)
    hot_news = models.HotNews.objects.select_related('news').only('news__title',
    'news__image_url','news_id').filter(is_delete=False).order_by('priority',
    '-news__click')[0:3]

    # return render(request,'news/index.html',context={
    #     'tags':tags
    # })
    return render(request,'news/index.html',locals())


def demo(request,id):
    res = "<h1 style='color:red'> four in the morning %s </h1> "
    return HttpResponse(res % id)


# 新闻列表
class NewsListView(View):
    def get(self,request):
        """
        tag_id
        page
        route: /news/
        :param request:
        :return:
        http://127.0.0.1:8000/?tag_id=0&page=1
        """
        # 1, 获取前台传的参数， 查询字符串
        try:
            tag_id = int(request.GET.get('tag_id',0 ))
        except Exception as e:
            logger.error('标签错误\n{}'.format(e))
            tag_id=0
        try:
            page = int(request.GET.get('page',1))
        except Exception as e:
            logger.error('页面错误\n{}'.format(e))
            page = 1
        # news_list = models.News.objects.select_related('tag','author').only('id','image_url','title','digest','author__username','tag__name','update_time').filter(is_delete=False)

        # 1- 6
        news_list = models.News.objects.values('id','title','image_url','digest','update_time').annotate(tag_name=F('tag__name'), author=F('author__username'))
        news = news_list.filter(is_delete=False,tag_id=tag_id) or news_list.filter(is_delete=False)
        # 分页
        paginator = Paginator(news,3)
        try:
            news_info = paginator.page(page)
        except Exception as e:
            logger.info('给定的页码错误{}'.format(e))
            news_info = paginator.page(paginator.num_pages)
        # news_info_list = []
        # for n in news_info:
        #     news_info_list.append({
        #         'id':n.id,
        #         'title':n.title,
        #         'digest':n.digest,
        #         'author':n.author.username,
        #         'image_url':n.image_url,
        #         'tag_name':n.tag.name,
        #         'update_time':n.update_time.strftime('%Y年%m月%d日 %H:%M')
        #     })
        data = {
            'news': list(news_info),
            'total_pages':paginator.num_pages
        }
        return to_json_data(data=data)


#新闻详情，传送news_id的值
class News_detail(View):
    def get(self,request,news_id):

        news = models.News.objects.select_related('tag','author').only('title', 'content', 'update_time', 'tag__name', 'author__username').\
            filter(is_delete=False, id=news_id).first()


        comments = models.Comments.objects.select_related('author','parent').only(
            'author__username','update_time','parent__author__username','content'
        ).filter(is_delete=False,news_id=news_id)

        comments_list = []
        for i in comments:
            comments_list.append(
                i.to_data()
            )

        if news:
            return render(request,'news/news_detail.html',context={
                'news':news,
                'comments_list':comments_list,
            })
        else:
            return HttpResponseNotFound('PAGE NOT FOUND')


class BannerView(View):
    def get(self,request):
        # banners = models.Banner.objects.select_related('news').only('image_url',
        # 'news__title','news_id').filter(is_delete=False)[0:6]
        banners = models.Banner.objects.values('image_url').annotate(news_id=F(
        'news_id'),news_title =F('news__title')).filter(is_delete=False)[0:6]


        # banner_info=[]
        # for i in banners:
        #     banner_info.append({
        #         'image_url':i.image_url,
        #         'news_id':i.news_id,
        #         'news_title':i.news.title,
        #     })

        data = {
            'banners':list(banners)

        }
        return to_json_data(data=data)


class CommentView(View):
    def post(self,request,news_id):
        """
        1，判断用户是否登录
        2，获取参数
        3，效验参数
        4，保存到数据库
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            return to_json_data(errno=Code.SESSIONERR,errmsg=error_map[Code.SESSIONERR])

        if models.News.objects.only('id').filter(is_delete=False,id=news_id).exists():
            return to_json_data(errno=Code.PARAMERR,errmsg='新闻不存在')

        #获取参数
        json_str = request.body
        if not json_str:
            return to_json_data(errno=Code.PARAMERR, errmsg='参数错误')

        dict_data = json.loads(json_str)

        #一级评论
        content = dict_data.get('content')
        if not dict_data.get('content'):
            return to_json_data(errno=Code.PARAMERR,errmsg='评论数据不能为空')

        #回复评论
        pt_id = dict_data.get('parent_id')
        try:
            if pt_id:
                if models.Comments.objects.only('id').filter(is_delete=False,id=pt_id,
            news_id=news_id).exists():
                    return to_json_data(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])

        except Exception as e:
            logging.info('前台传的parent_id异常{}'.format(e))
            return to_json_data(errno=Code.PARAMERR,errmsg='未知错误')

        #保存到数据库
        news_content = models.Comments()
        news_content.content=content
        news_content.news_id=news_id
        news_content.author=request.user
        news_content.parent_id=pt_id if pt_id else None
        news_content.save()
        #序列化返回
        return to_json_data(data=news_content.to_data())



