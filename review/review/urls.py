"""review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# 引入资源文件
from django.views import static

from review import settings
# 引入页面模板
from review.controller import index, home, add, review, user, result

urlpatterns = [
    # 首页路由
    url(r'^$', index.index),
    url(r'^index$', index.index),
    url(r'^login$', index.login),
    url(r'^logout$', index.logout),
    # home模板路由
    url(r"^home$", home.home),
    url(r'^add_score$', home.add),
    # add模块路由、公司管理
    url(r'^add$', add.add),
    url(r'^add01$', add.add01),
    url(r'^add02$', add.add02),
    # review模块路由
    url(r'^review$', review.review),
    url(r'^add_review$', review.add_review),
    url(r'^del_review$', review.del_review),
    # 用户管理木块路由
    url(r'^user$', user.user),
    url(r'^de_del$', user.de_del),
    url(r'^user_del$', user.user_del),
    # 打分详情管理
    url(r'^result$', result.result),
    url(r'^detail$', result.detail),
    # 添加样式文件位置
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_URL}, name='static'),

]
