from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from crm import form
from crm import models
import hashlib
from rbac.service.permission import init_permission


def index(request):
    return HttpResponse("dsahdkaslkdlaskjlkasjldjasd成功了 ")


def login(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        md5 = hashlib.md5()  # md5加密
        md5.update(pwd.encode("utf-8"))
        pwd = md5.hexdigest()
        obj = models.UserProfile.objects.filter(username=uname, password=pwd, is_active=True).first()  # 验证密码
        if obj:
            request.session["u_id"] = obj.pk  # 添加session
            init_permission(request, obj)
            return redirect(reverse('list'))
        else:
            return render(request, "login.html", {"arror": "用户或密码输入错误!!!"})
    return render(request, "login.html")


# 注册
def reg(request):
    if request.method == "POST":
        form_obj = form.Forms(request.POST)
        # print ( form_obj.is_valid () )
        if form_obj.is_valid():  # 判断有没有 error
            form_obj.save()
            return redirect(reverse("login"))
    else:
        form_obj = form.Forms()
    return render(request, "reg.html", {"from_obj": form_obj})
