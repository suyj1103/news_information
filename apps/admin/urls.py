from . import views

from django.urls import path

app_name = 'admin'

urlpatterns = [
    path('index',views.IndexView.as_view(),name='index'),
]