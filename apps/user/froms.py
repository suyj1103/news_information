import re
from django.contrib.auth import login
from django.db.models import Q
from django import forms
from .models import Users
from django_redis import get_redis_connection
from . import contants
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=20,min_length=5,
                               error_messages={
                                   'min_length':'用户名长度大于5',
                                   'max_length':'用户名长度小于20',
                                   'required':'用户名不能为空'
                               })
    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度要大于6",
                                               "max_length": "密码长度要小于20",
                                               "required": "密码不能为空"}
                               )
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6,
                                      error_messages={"min_length": "密码长度要大于6",
                                                      "max_length": "密码长度要小于20",
                                                      "required": "密码不能为空"}
                                      )
    mobile = forms.CharField(label='手机号', max_length=11, min_length=11,
                             error_messages={"min_length": "手机号长度有误",
                                             "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})

    sms_code = forms.CharField(label='短信验证码', max_length=6, min_length=6,
                               error_messages={"min_length": "短信验证码长度有误",
                                               "max_length": "短信验证码长度有误",
                                               "required": "短信验证码不能为空"})

    def clean_mo_un(self):
        users = self.cleaned_data.get('username')
        tel = self.cleaned_data.get('mobile')
        if Users.objects.filter(username=users,mobile=tel).exists():
            raise forms.ValidationError('用户名或手机号已注册，请重新输入')
        return users , tel


    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password')
        passwd_rep =cleaned_data.get('password_repeat')

        if passwd != passwd_rep:
            raise forms.ValidationError('密码不一致')

        tel = cleaned_data.get('mobile')
        sms_text = cleaned_data.get('sms_code')

        # 连接redis
        redis_conn = get_redis_connection('verify_codes')

        real_sms = redis_conn.get('sms_{}'.format(tel).encode('utf8'))

        if (not real_sms) or (sms_text != real_sms.decode('utf8')):
            raise forms.ValidationError('短信验证码错误')


class LoginFrom(forms.Form):
    user_account = forms.CharField()
    password = forms.CharField(label='密码',max_length=20,min_length=6,
                               error_messages= {
                                'max_length':'密码长度小于20',
                                'min_length':'密码长度大于6',
                                'required':'密码不能为空'}
                               )
    remember_me = forms.BooleanField(required=False)

    # 复用表单
    def __init__(self,*args,**kwargs):

        self.request = kwargs.pop('request',None)
        super(LoginFrom,self).__init__(*args,**kwargs)


    def clean_user_account(self):
        user_info = self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('用户账号不能为空')

        if not re.match(r'^1[3-9]\d{9}$', user_info) and (len(user_info)<5 or len(user_info)>20):
            raise forms.ValidationError('用户账号格式不正确，请重新输入')
        return user_info

    def clean(self):
        cleaned_data = super().clean()
        user_info = cleaned_data.get('user_account')
        passwd = cleaned_data.get('password')
        hold_login = cleaned_data.get('remember_me')

        # 查询 用户名 手机号 user_info 手机号  用户名
        user_queryset = Users.objects.filter(Q(mobile=user_info) | Q(username=user_info))
        if user_queryset:
            user = user_queryset.first()
            if user.check_password(passwd):
                # a = self.request.session
                # a.set_expiry(constants.USER_SAVE_TO_SESSION) if hold_login else a.set_expiry(0)
                if hold_login:
                 # 加入勾选框有值
                    self.request.session.set_expiry(contants.USER_SAVE_TO_SESSION)  # none 默认是14天
                else:
                    self.request.session.set_expiry(0)
                login(self.request,user)
            else:
                raise forms.ValidationError('密码错误，请重新输入')
        else:
            raise forms.ValidationError('用户账号不存在，请重新输入')
