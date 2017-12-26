from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser
from review.util import util


# 首页模块
def index(request):
    # 检测用户是不是已经登录,如果已经登录,直接跳转到首页
    if util.get_user(request, 'id'):
        return HttpResponseRedirect('/home')

    context = {}
    context['title'] = "蓝血360评测系统"
    login_info = request.session.get("login", '')
    context['login_info'] = login_info
    request.session['login'] = ''
    return render(request, 'index.html', context)


# 登录模块
def login(request):
    login_result = ''
    username = request.POST['username']
    password = request.POST['password']
    if username and password:
        password = util.md5(password)
        # 查询数据库是否可以登录

        login_res = ReviewUser.objects.filter(email=username, password=password)
        if login_res:
            request.session['user_info'] = login_res.all().values('id', 'name', 'email').first()
            return HttpResponseRedirect('/home')
        else:
            login_result = "用户名或密码错误"
        request.session['login'] = login_result
    else:
        res = util.result(request, False, '用户名或密码不得为空', '', 3)
        return res
    return HttpResponseRedirect('/index')


# 用户退出
def logout(request):
    if request.session.get("user_info", None) is not None:
        del request.session['user_info']

    return HttpResponseRedirect('/index')
