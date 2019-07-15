from django.middleware.clickjacking import XFrameOptionsMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import re


class AuthMiXin(MiddlewareMixin):

    def process_request(self, request):
        url = request.path_info
        request.current_menu_id = None
        login = request.session.get("is_login")
        request.breadcrumb_list = [{'title': '首页', 'url': '/index/'}]
        # 判断白名单
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return
        # 判断是不是登陆过的
        if not login:
            return redirect("login")
        # 免登录
        for i in settings.NO_PERMISSION_LIST:
            if re.match(i, url):
                return

        obj_list = request.session.get("permission")
        # 判断权限
        for i in obj_list.values():
            if re.match(f'^{i["url"]}$', url):
                pid = i.get("parent")
                id = i.get("id")
                pname = i.get("pname")
                if pid:
                    request.current_menu_id = pid  # 获取到 parent 的id
                    parent = obj_list[pname]
                    request.breadcrumb_list.append ( {'url': parent['url'], 'title': parent['title']} )
                    request.breadcrumb_list.append({"url": i["url"], "title": i["title"]})
                else:
                    request.current_menu_id = id  # 获取到 自己的id
                    request.breadcrumb_list.append({"url": i["url"], "title": i["title"]})
                return

        return HttpResponse("你没有权限")
