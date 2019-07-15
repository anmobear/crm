from django.http.request import QueryDict
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from crm import form
from crm import models
from utils.pagination import Pagination
from django.db.models import Q
from django.db import transaction
from django.conf import settings


# 展示客户页面  公私户
class CustomerList(View):
    # get请求页面
    def get(self, request):
        q = self.search(["name", "qq"])
        if request.path_info == reverse("list"):
            customer = models.Customer.objects.filter(q, consultant__isnull=True, )  # 显示共户的内容
        else:
            customer = models.Customer.objects.filter(q, consultant=request.user_obj)  # 展示私户的内容
        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(customer), request.GET.copy(), 2)  # 掉用分页的方法
        # print(pag.page_num)
        return render(request, "customer/customer_list.html",
                      {"customer_obj": customer[pag.start:pag.end], "ret": pag.page_html})

    def post(self, request):
        action = request.POST.get("action")
        # print(action)
        if hasattr(self, action):
            ret = getattr(self, action)()  # 利用反射调用公司户的转换
            if ret:
                return ret
        return self.get(request)

    # 公户转私户
    def multi_apply(self):
        ids = self.request.POST.get("ids", "")
        count = models.Customer.objects.filter(consultant=self.request.user_obj).count()
        if (count + len(ids)) > settings.MAX_CUSTOMERS:  # 限制私户的客户数量
            return HttpResponse("你客户太多了 先把现在客户成单了")
        with transaction.atomic():
            # 加行级锁select_for_update
            queryset = models.Customer.objects.filter(pk__in=ids, consultant__isnull=True).select_for_update()
            if len(queryset) == len(ids):
                queryset.update(consultant=self.request.user_obj, )
            else:
                return HttpResponse("你的客户被别人抢走了")

    # 私户转公户
    def multi_pub(self):
        ids = self.request.POST.get("ids", "")
        models.Customer.objects.filter(pk__in=ids).update(consultant=None)

    # q 方法使用函数
    def search(self, field_list):
        query = self.request.GET.get("query", "")
        q = Q()
        q.connector = "OR"
        for i in field_list:
            # Q(Q(name__contains=query)|Q(qq__contains=query ))
            # q.children.append(Q(('{}__contains'.format(i),query)))
            q.children.append(Q((f"{i}__contains", query)))
        return q


# 编辑添加
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()  # 取信息的对象
    from_obj = form.AddForm(instance=obj)
    if request.method == "POST":
        from_obj = form.AddForm(request.POST, instance=obj)  # 吧POST请求交给modelform对象
        if from_obj.is_valid():
            from_obj.save()  # models 直接生成input标签
            taxt = request.GET.get("next")
            return redirect(taxt)  # 重定向到 customer_list 页面里面
    stutas = "编辑客户" if edit_id else "添加客户"  # 用三元表达式你要判断的
    return render(request, "customer/customer_edit.html", {"form_obj": from_obj, "stutas": stutas})
