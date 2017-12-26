from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser, ReviewCount, ReviewScore
from django.db import connection
import datetime
from review.util import util
import time


# 查看所有评选, 以及显示页面
def review(request):
    if util.base(request) != False:
        return util.base(request)
    context = util.user(request)
    context['review'] = all_review()
    return render(request, 'review.html', context)


def add_review(request):
    name = request.POST['name']
    if util.not_empty(name):
        # 查询当天是否存在评选
        in_px = ReviewCount.objects.filter(overtime__gte=time.time()).all().values('id')
        if in_px:
            return util.result(request, False, "当天已存在评选主题，请删除后再试")
        else:
            c = ReviewCount()
            c.name = name
            c.starttime = time.time()
            # 取得当天晚24点的时间戳，确保每一次评选只能到凌晨截止
            c.overtime = time.mktime(
                time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time() + float(24 * 3600))),
                              '%Y-%m-%d %H:%M:%S'))
            c.save()
            return HttpResponseRedirect('./review')
    else:
        return util.result(request, False, "暂无评选主题")


def del_review(request):
    id = int(request.GET['id'])
    if id > 0 and util.not_empty(id):
        c = ReviewCount(id=id)
        c.delete()
        return HttpResponseRedirect('./review')
    else:
        return util.result(request, False, "参数错误!")


# 查询当前存在的所有评选
def all_review():
    res = ReviewCount.objects.all().values().order_by("-starttime")
    for c in res:
        c["starttime"] = util.get_time(c["starttime"])
        c["overtime"] = util.get_time(c["overtime"])
    return res
