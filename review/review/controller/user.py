from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser, ReviewCount, ReviewScore, ReviewDeparment
from django.db import connection
import time
from review.controller import home
from review.util import util


def user(request):
    if util.base(request) != False:
        return util.base(request)
    context = util.user(request)
    context['de'] = all_de()
    context['user'] = home.user()
    return render(request, 'user.html', context)


# 删除部门(和以下删除用户可联合使用，但此处不做处理)
def de_del(request):
    id = int(request.GET['id'])
    if id > 0 and util.not_empty(id):
        de = ReviewDeparment(id=id)
        de.delete()
    else:
        return util.result(request, False, '参数错误')
    return HttpResponseRedirect("/user")


# 删除用户
def user_del(request):
    id = int(request.GET['id'])
    if id > 0 and util.not_empty(id):
        de = ReviewUser(id=id)
        de.delete()
    else:
        return util.result(request, False, '参数错误')
    return HttpResponseRedirect("/user")


# 查询所有的部门
def all_de():
    de = ReviewDeparment.objects.all()
    return de
