
from django.shortcuts import render
# Create your views here.
from django.views import View
import logging
from . import models
logger = logging.getLogger('django')
from django.http import HttpResponse,Http404

def course_url(request):
    courses = models.Course.objects.only('title','cover_url','teacher__name').filter(is_delete=False)
    return render(request,'course/course.html',context={
        'courses':courses
    })



class CourseDetail(View):

    def get(self,request,course_id):
        try:
            course = models.Course.objects.only('title','cover_url','video_url','profile',
            'outline','teacher__name','teacher__positional_title','teacher__avatar_url',
            'teacher__profile').select_related('teacher').filter(is_delete=False,id=course_id).first()

        except models.Course.DoesNotExist as e:
            logger.info('当前课程出现异常')
            raise Http404('课程不存在')


        return render(request,'course/course_detail.html',locals())


