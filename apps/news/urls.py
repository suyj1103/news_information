from django.urls import path
from . import views
app_name = 'news'
urlpatterns = [
    path('',views.index,name='index'),
    path('<int:id>',views.demo),
    path('news/',views.NewsListView.as_view(),name='news_list'),
    path('news/<int:news_id>/', views.News_detail.as_view(), name='news_detail'),
    path('news/banners/',views.BannerView.as_view(),name='banners'),
    path('news/<int:news.id>/comments/',views.CommentView.as_view(),name='comments'),

]
