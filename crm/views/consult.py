from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from crm import form
from crm import models
from utils.pagination import Pagination


class ConsultList(View):
    # get请求页面
    def get(self, request, *args, **kwargs):
        query = request.GET
        customer_id = kwargs.get("customer_id")
        q = self.search([])
        if customer_id:
            consult = models.ConsultRecord.objects.filter(q, customer_id=customer_id, consultant=request.user_obj,
                                                          delete_status=False)
        else:
            consult = models.ConsultRecord.objects.filter(q, consultant=request.user_obj, delete_status=False)
        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(consult), request.GET.copy(), 2)  # 调用分页的
        # print(pag.page_num)
        return render(request, "customer/consult_list.html",
                      {"consult_obj": consult[pag.start:pag.end], "ret": pag.page_html})

    def post(self, request, *args, **kwargs):

        return self.get(request, *args, **kwargs)

    def search(self, field_list):
        query = self.request.GET.get("query", "")
        q = Q()
        q.connector = "OR"
        for i in field_list:
            # Q(Q(name__contains=query)|Q(qq__contains=query ))
            # q.children.append(Q(('{}__contains'.format(i),query)))
            q.children.append(Q((f"{i}__contains", query)))
        return q


def consult_add(request):
    obj = models.ConsultRecord(consultant=request.user_obj)
    form_obj = form.ConsultForm(instance=obj)
    if request.method == "POST":
        form_obj = form.ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get("next")
            return redirect(next)
    return render(request, 'customer/consult_add.html', {"form_obj": form_obj})


def consult_edit(request, edit_id):
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()  # 找到edit_id 对应的pk
    form_obj = form.ConsultForm(instance=obj)
    if request.method == "POST":
        form_obj = form.ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            text = request.POST.get("text")
            return redirect(text)
    return render(request, 'customer/consult_edit.html', {"form_obj": form_obj})


def consult_change(request, edit_id=None):
    if edit_id:
        obj = models.ConsultRecord.objects.filter(pk=edit_id).first()  # 找到edit_id 对应的pk
    else:
        obj = models.ConsultRecord(consultant=request.user_obj)  # 这个是添加的
    title = "修改跟进记录" if edit_id else "添加跟进记录"
    form_obj = form.ConsultForm(instance=obj)
    if request.method == "POST":
        form_obj = form.ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            text = request.POST.get("text")
            return redirect(text)
    return render(request, 'froms.html', {"form_obj": form_obj, "title": title})
