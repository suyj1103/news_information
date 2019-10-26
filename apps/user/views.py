from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from utils.res_code import to_json_data, Code, error_map
# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.views import View
from .froms import RegisterForm, LoginFrom
from .models import Users
import json
from django.contrib.auth import login, logout


class Register(View):
    def get(self, request):

        return render(request, 'users/register.html')

    def post(self, request):
        """
        用户名
        密码
        确认密码
        mobile
        短信验证码
        :param request:
        :return:
        """
        json_str = request.body
        if not json_str:
            return to_json_data(errno=Code.PARAMERR, errmsg='参数错误')
        data_dict = json.loads(json_str.decode('utf8'))
        form = RegisterForm(data=data_dict)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')
            user = Users.objects.create_user(username=username, password=password, mobile=mobile)

            # 第一个参数 request obj  第二个 user obj
            # 注册成功把用户id 保存到session里面  session_id 返回给cookie
            login(request, user)
            return to_json_data(errmsg='注册成功')

        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)
            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)


class Login(View):
    # @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        json_str = request.body
        if not json_str:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        data_dict = json.loads(json_str)
        form = LoginFrom(data=data_dict, request=request)

        if form.is_valid():
            return to_json_data(errmsg='登录成功')

        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)
            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)


# 登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))
