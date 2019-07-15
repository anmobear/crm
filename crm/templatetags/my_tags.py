from django import template
from django.urls import reverse
from django.http.request import QueryDict
register = template.Library()


@register.simple_tag
def reverse_url(request, urlname, *args, **kwargs):
    text = request.get_full_path()      # 获取携带的url
    qd = QueryDict(mutable=True)        # QueryDict默认是不可变的 实例化对象把 mutable
    qd["next"] = text   # 把他加到QueryDict 类型的字典中
    base_url = reverse(urlname, args=args, kwargs=kwargs)   # 获取调用函数的url
    # print(base_url, qd.urlencode())
    return f"{base_url}?{qd.urlencode()}"    # 将拼接好的url返回给模板显示




