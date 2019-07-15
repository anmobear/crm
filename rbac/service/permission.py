from django.shortcuts import render, redirect,HttpResponse
from collections import OrderedDict
from django.conf import settings


# 初始化
def init_permission(request, obj):
    if not obj:
        return render(request, "login.html", {"error": "用户名或密码错误!"})
    permission_obj = obj.roles.filter(permissions__url__isnull=False).values(   # 找到不能为空的
        "permissions__url",
        "permissions__title",
        "permissions__menu__title",
        "permissions__menu__icon",
        "permissions__menu_id",
        "permissions__id",
        "permissions__name",
        "permissions__menu__wight",
        "permissions__parent_id",
        "permissions__parent__name",
    ).distinct()   # 去重复

    dic = OrderedDict()    # 创建一个有序字典

    permission_dict = {}    # 创建权限的字典
    menu_list = {}          # 菜单字典
    # print(permission_obj)
    for i in permission_obj:
        # 构造权限的数据类型
        permission_dict[i["permissions__name"]] = ({"url": i["permissions__url"],
                                                    "parent": i["permissions__parent_id"],
                                                    "id": i["permissions__id"],
                                                    "title": i["permissions__title"],
                                                    'name': i["permissions__name"],
                                                    'pname': i["permissions__parent__name"],
                                                    })
        menu_id = i["permissions__menu_id"]   # 找到用户权限里面的有菜单的
        if not menu_id:
            continue
        menu_list.setdefault(menu_id, {"url": i["permissions__url"],
                                       "title": i["permissions__menu__title"],
                                       "wight": i["permissions__menu__wight"],
                                       "id": i["permissions__id"],
                                       "icon": i['permissions__menu__icon'], "children": []
                                       },)
        menu_list[menu_id]["children"].append({
            "title": i["permissions__title"],
            "url": i["permissions__url"],
            "id": i["permissions__id"],
        })
    request.session[settings.MENU_SESSION_KEY] = menu_list

    # print(request.session["menu"])
    request.session["is_login"] = True
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict



