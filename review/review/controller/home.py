from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import ReviewUser, ReviewCount, ReviewScore
from django.db import connection
import time
from review.util import util


# 首页模板以及数据查询
def home(request):
    if util.base(request) !=False:
        return util.base(request)

    context = util.user(request)

    user_data = []
    # 查询是否有评选会议
    if in_px():
        context['in_name'] = in_px().name
        context['in_id'] = in_px().id
        # 查询所有用户打分详情
        for u in user():
            rs = ReviewScore.objects.filter(uid=u['id'], cid=in_px().id, did=util.get_user(request, 'id')).values(
                'score',
                'count').first()
            if rs is not None:
                if rs['score'] is not None:
                    u['score'] = rs['score']
                if rs['count'] is not None:
                    u['count'] = rs['count']
            user_data.append(u)
    else:
        context['in_name'] = False
    context['user'] = user_data
    return render(request, 'home.html', context)


def add(request):
    score = float(request.GET['score'])

    if score > 100 or score < 0:
        json = util.print_json(1000, '您输入的分数不符合要求', '')
    else:
        # 声明全局对象
        count = 0
        reviewScore = None

        review_select = ReviewScore.objects.filter(uid=str(request.GET['id']), did=str(util.get_user(request, 'id')),
                                                   cid=str(request.GET['pid'])).values('id', 'count').first()
        print("查询数据打分数据-->", review_select)
        if review_select:
            if int(review_select['count']) >= 3:
                json = util.print_json(1000, '同一个同事每人最多打分3次', '')
                return HttpResponse(json)
            else:
                count = review_select['count'] + 1
                if count == '':
                    count = 1
                reviewScore = ReviewScore(id=review_select['id'])
        else:
            count = 1
            reviewScore = ReviewScore()

        # 分数
        reviewScore.score = score
        # 打分对象
        reviewScore.uid = int(request.GET['id'])
        # 打分人、即登录用户
        reviewScore.did = int(util.get_user(request, 'id'))
        # 第多少期评选
        reviewScore.cid = int(request.GET['pid'])
        # 打分时间
        reviewScore.time = time.time()
        # 打分次数
        reviewScore.count = int(count)
        # 保存数据
        reviewScore.save()
        json = util.print_json(1, '', )
    return HttpResponse(json)


# 查询当前有没有评选项目
def in_px():
    try:
        # 查询当前唯一的评测
        result = ReviewCount.objects.distinct().get(overtime__gte=int(time.time()))
    except ReviewCount.DoesNotExist:
        result = False
    except ReviewUser.MultipleObjectsReturned:
        # 多条数据则提示错误
        result = False
    # print("查询语句：", connection.queries)
    return result


# 查询所有用户
def user():
    result = ReviewUser.objects.all().values('id', 'name', 'deparment', 'email', 'bz')
    print("查询用户信息:", result)
    return result
