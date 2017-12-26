# 工具类
from django.shortcuts import render
import logging
import json
import time
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# 编写MD5方法
def md5(data):
    import hashlib
    m = hashlib.md5(str(data).encode(encoding='gb2312'))
    return m.hexdigest()


# 返回全局的用户数据
def user(request):
    context = {}
    context['user_name'] = get_user(request, 'name')
    context['user_email'] = get_user(request, 'email')
    return context


# 默认检测用户是否有登录状态
def base(request):
    if get_user(request, "id") is None:
        return result(request, False, '登录超时', '/logout', 3)
    else:
        return False


# 查询用户信息
def get_user(request, key=''):
    rs = request.session.get('user_info', None)
    if rs is not None and key in rs:
        return rs[key]
    else:
        return None


# 生成JSON串
def print_json(code=1000, msg='', data=''):
    json_result = {}
    json_result['code'] = code
    json_result['msg'] = msg
    if type(data) == list:
        json_result['data'] = data
    else:
        if data:
            json_result['data'] = [data]
        else:
            json_result['data'] = ''

    return json.dumps(json_result)


# 字符串为空检测
def not_empty(str):
    if str is not None and str != '':
        return True
    return False


# 时间戳转换
def get_time(data_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_time))


# 页面跳转模块,成功和失败两方面
# success：是否为显示成功模板
# message：给用户的通知信息
# page: 要跳转的页面 默认为index
# relay：跳转延时,默认为5s
def result(request, success=True, message='暂无提示信息', page='', relay=3):
    print("result is run")
    # 如果页面为空或者未result页面，则默认返回上一页
    if page == '' or page == 'result':
        menu = "<script>document.getElementById('href').href=document.referrer</script>"
    else:
        menu = ''
    # 返回动态数据
    context = {}
    context['message'] = message
    context['page'] = page
    context['success'] = success
    context['relay'] = relay
    context['menu'] = menu
    return render(request, 'result.html', context)


# 输出日志
def log(code=5, message=''):
    if code == 1:
        logging.debug(message)
    elif code == 2:
        logging.info(message)
    elif code == 3:
        logging.warning(message)
    elif code == 4:
        logging.error(message)
    else:
        logging.critical(message)
