# 编写自定义的模板函数

from django import template

register = template.Library()


@register.filter(name='get_time')
def get_time(time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time)