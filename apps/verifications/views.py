import random

from django.shortcuts import render
from django_redis import get_redis_connection
from . import forms
from utils.captcha.captcha import captcha
# Create your views here.
from django.views import View
from django.http import HttpResponse, JsonResponse
import logging
import json
logger = logging.getLogger('django')
from user.models import Users
from utils.res_code import to_json_data, error_map, Code
# from utils.yuntongxun.sms import CCP
from celery_tasks.sms import task
from . import constants

class Image_code(View):
    def get(self, request, image_id):
        """
        1, 图形验证保存到数据库
            连接数据库
            保存
            hash  string set zset  l
        :param request:
        :param image_id:
        :return:
        """
        text, image = captcha.generate_captcha()
        con_redis = get_redis_connection('verify_codes')
        redis_key = 'img_{}'.format(image_id)

        con_redis.setex(redis_key, 300, text)
        logger.info('图片验证码:     {}'.format(text))
        return HttpResponse(content=image, content_type='image/jpeg')


class UsernameView(View):
    def get(self, request, username):
        """
        route:  username/(?<username>\w{5,20})/
            \w  匹配字母 数字 下划线
            {"errno":"0","errmsg":" ", "data":{
            "username":"admin",
            "count":0
            }}
        :return  json object
        :param request:
        :param username:
        :return:
        """
        count = Users.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }
        # return JsonResponse({'data':data})
        return to_json_data(data=data)


class MobileView(View):
    """
     mobile
     route: mobiles/(?P<mobile>1[3-9]\d{9})/
    """

    def get(self, request, mobile):
        # mobile = reques.GET.get('mobile')
        data = {
            'count': Users.objects.filter(mobile=mobile).count(),
            'mobile': mobile
        }
        return to_json_data(data=data)


class Sms_code(View):
    """
    1, 校验图片是否正确
    2，判断60秒是否有发送记录
    3 构造6位短信验证码
    4，保存到数据库
    5， 发送短信
    """

    def post(self,request):
        " mobile  text  image_code_id"
        json_str  = request.body
        if not json_str:
            return to_json_data(errno=Code.PARAMERR,errmsg='参数为空')
        dict_data = json.loads(json_str)
        form = forms.FromRegister(data=dict_data)

        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            # 生成6位短信验证码
            sms_num = '%06d' % random.randint(0,constants.RANDOM_TEMPLATE)

            # 构建外键
            con_redis = get_redis_connection('verify_codes')
            # 短信建  5分钟  sms_num
            sms_text_flag = "sms_{}".format(mobile).encode('utf8')
            # 过期时间
            sms_flag_fmt = 'sms_flag_{}'.format(mobile).encode('utf8')
            # 存
            con_redis.setex(sms_text_flag,constants.SMS_CODE_EXPIRES,sms_num)
            con_redis.setex(sms_flag_fmt,constants.SMS_CODE_EXPIRES_TIME,constants.SMS_TEMPLATE)  # 过期时间  1



            # 发送短信
            logger.info('短信验证码：{}'.format(sms_num))

            # 使用celery 异步发送短信
            # expires  =constants.SMS_CODE_EXPIRES
            # task.send_sms_code.delay(mobile,sms_num,expires,constants.SMS_TEMPLATE)
            # return to_json_data(errmsg='短信验证码发送成功')

            logging.info('发送短信验证码正常[mobile:%s,sms_num:%s]'% (mobile,sms_num))
            return to_json_data(errmsg='短信验证码发送成功')
            # try:
            #     result = CCP().send_template_sms(mobile,[sms_num,5],1)
            # except Exception as e:
            #     logger.error('发送短信异常[mobile : %s message: %s]'% (mobile,e))
            #     return to_json_data(errno=Code.SMSERROR,errmsg=error_map[Code.SMSERROR])
            # else:
            #     if result == 0:
            #         logger.info('发送短信验证码成功[mobile : %s sms_code: %s]'% (mobile,sms_num))
            #         return to_json_data(errmsg='短信验证码发送成功')
            #     else:
            #         logger.warning('发送短信失败 mobile: {}'.format(mobile))
            #         return to_json_data(errno=Code.SMSFAIL,errmsg=error_map[Code.SMSFAIL])

        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)
            return to_json_data(errno=Code.PARAMERR,errmsg=err_msg_str)

