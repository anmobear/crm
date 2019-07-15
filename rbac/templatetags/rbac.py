from collections import OrderedDict
from django.conf import settings
from django import template

# register
register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    ordered_dict = OrderedDict()
    # 当前的url
    url = request.path_info
    menu_list = request.session["menu"]

    ret = sorted(menu_list, key=lambda x: menu_list[x]['wight'], reverse=True)
    for i in ret:
        ordered_dict[i] = menu_list[i]

    for item in ordered_dict.values():
        item["class"] = "hide"
        for j in item["children"]:
            if request.current_menu_id == j["id"]:
                # if re.match(f"^{j['url']}$", url):
                j["class"] = "active"
                item["class"] = " "

    return {"menu_list": ordered_dict.values()}

    # @register.inclusion_tag("menu.html")
    # def menu(request):
    #     url = request.path_info()
    #     obj_list = request.session["permission"]
    #     for i in obj_list:
    #         if re.match ( "^{}$".format ( i['url'] ), url ):
    #             i['class'] = 'active'
    #     return {'menu_list': obj_list}
    #


@register.inclusion_tag("rbac/daohang.html")
def haohang(request):
    return {'breadcrumb_list': request.breadcrumb_list}


@register.filter
def has_permission(request, name):
    permission_dict = request.session[settings.PERMISSION_SESSION_KEY]
    if name in permission_dict:
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()  # uid=1
    params['rid'] = rid  # rid = 1
    return params.urlencode()  # uid=1&rid = 1
