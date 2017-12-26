# 用户及部门添加控制器
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser, ReviewCount, ReviewScore, ReviewDeparment
from django.db import connection
import time
from review.util import util


def add(request):
    if util.base(request) != False:
        return util.base(request)

    context = util.user(request)
    context['department'] = department()

    # 通过d_id和u_id确认分辨是否是新增还是修改
    if "d_id" in request.GET:
        d_id = int(request.GET["d_id"])
        # 通过页面传值处理相应数据的渲染
        if d_id and util.not_empty(d_id):
            context['department_value'] = ReviewDeparment.objects.filter(id=d_id).first().name
            context['d_id'] = d_id
    if "u_id" in request.GET:
        u_id = int(request.GET['u_id'])
        if u_id and util.not_empty(u_id):
            context['user_value'] = ReviewUser.objects.filter(id=u_id).first()
            context['u_id'] = u_id
            print("test:", context['user_value'])

    return render(request, 'add.html', context)


def add01(request):
    department_name = request.POST['name']
    d_id = int(request.GET['d_id'])
    if util.not_empty(department_name):
        print("d_id is :", d_id)
        if d_id > 0:
            d = ReviewDeparment(id=d_id)
        else:
            d = ReviewDeparment()
        d.name = department_name
        d.save()
        # print("保存结果:", d.save(), "上传结果：", department_name)
        # 如果是新增则跳转到添加页面，修改则跳到管理页面
        if d_id > 0:
            return HttpResponseRedirect('/user')
        else:
            return HttpResponseRedirect('/add')

    else:
        return util.result(request, False, '部门名称不得为空', '')


def add02(request):
    name = request.POST['name']
    email = request.POST['email']
    de = request.POST['de']
    bz = request.POST['bz']

    u_id = int(request.GET['u_id'])

    if util.not_empty(name) and util.not_empty(email) and util.not_empty(de) and util.not_empty(bz):
        if u_id > 0:
            user = ReviewUser(id=u_id)
        else:
            user = ReviewUser()

        user.email = email
        user.name = name
        user.deparment = de
        user.password = util.md5(1)
        user.bz = bz
        user.type = 2
        user.save()
        if u_id > 0:
            return HttpResponseRedirect('/user')
        else:
            return HttpResponseRedirect('/add')

    else:
        return util.result(request, False, '不得有空数据!', '')


# 查询所有部门
def department():
    return ReviewDeparment.objects.all().values()
