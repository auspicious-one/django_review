# 最终结果

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser, ReviewCount, ReviewScore, ReviewDeparment
from django.db import connection
import time
from review.controller import home
from review.util import util


# 查找每个人的具体分数
def result(request):
    if util.base(request) != False:
        return util.base(request)
    context = util.user(request)
    # 获取cid
    c_id = int(request.GET['c_id'])
    # 获取评选名称
    p_name = request.GET['name']
    context["p_name"] = p_name
    context['c_id'] = c_id

    # 获取所有用户信息并进行遍历,查询具体得分详情
    user = home.user()
    for u in user:
        # 通过用户uid 查询打分表，查出该用户打的所有分
        score = ReviewScore.objects.filter(uid=u['id'], cid=c_id).all().values("score", 'did')
        # 分辨统计各级别的人数以及总分
        bz_all = 0
        bz_count = 0
        zc_all = 0
        zc_count = 0
        pt_all = 0
        pt_count = 0
        # 遍历所有分数,按照规则取最终分
        for s in score:
            # 查询该用户的级别
            u_jb = ReviewUser.objects.filter(id=s['did']).values("bz").first()
            u_jb = int(u_jb["bz"])
            in_score = float(s["score"])
            if u_jb == 1:
                bz_all = bz_all + in_score
                bz_count += 1
            elif u_jb == 2:
                zc_all = zc_all + in_score
                zc_count += 1
            else:
                pt_all = pt_all + in_score
                pt_count += 1
        # 对不同级别求出平均值并累加,将结果赋予字典中
        if bz_count == 0:
            bz_all_avg = 0
        else:
            bz_all_avg = (bz_all / bz_count) * 0.4
        if zc_count == 0:
            zc_all_avg = 0
        else:
            zc_all_avg = (zc_all / zc_count) * 0.3
        if pt_count == 0:
            pt_all_avg = 0
        else:
            pt_all_avg = (pt_all / pt_count) * 0.3
        u['result'] = bz_all_avg + zc_all_avg + pt_all_avg
    context['user'] = user
    return render(request, 'score_result.html', context)


# 查询详情
def detail(request):
    if util.base(request) != False:
        return util.base(request)
    context = util.user(request)
    # 获取cid
    c_id = int(request.GET['c_id'])
    # 获取uid
    u_id = int(request.GET['u_id'])

    # 查询详情
    if util.not_empty(c_id) and util.not_empty(u_id):
        score_detail = ReviewScore.objects.filter(uid=u_id, cid=c_id).all().values("did", "score", "time")
        for d in score_detail:
            u = ReviewUser.objects.filter(id=d["did"]).values("name", "bz").first()
            d['name'] = u["name"]
            d["bz"] = u["bz"]
        context['score'] = score_detail
        return render(request, 'detail.html', context)
    else:
        return util.result(request, False, '参数错误')
