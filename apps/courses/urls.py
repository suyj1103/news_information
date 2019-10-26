from django.urls import path
from . import views
app_name = 'course'
urlpatterns = [
    path('',views.course_url,name = 'course'),
    path('<int:course_id>/',views.CourseDetail.as_view(),name='detail')
]
