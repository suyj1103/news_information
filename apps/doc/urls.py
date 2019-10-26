from django.urls import path
from . import views
app_name = 'doc'
urlpatterns = [
    path('',views.doc,name='docs'),
    path('download/<int:doc_id>/', views.DocDownload.as_view(), name='download'),


]