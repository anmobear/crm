from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.views import View
from crm import form
from crm import models
from utils.pagination import Pagination


class PaymentList(View):

    def get(self, request, *args, **kwargs):
        q = self.search([])
        payment = models.PaymentRecord.objects.filter(q, customer__consultant=request.user_obj, delete_status=False)

        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(payment), request.GET.copy(), 2)
        # print(pag.page_num)
        return render(request, "customer/payment_list.html",
                      {"payment_obj": payment[pag.start:pag.end], "ret": pag.page_html})

    def search(self, field_list):
        query = self.request.GET.get("query", "")
        q = Q()
        q.connector = "OR"
        for i in field_list:
            # Q(Q(name__contains=query)|Q(qq__contains=query ))
            # q.children.append(Q(('{}__contains'.format(i),query)))
            q.children.append(Q((f"{i}__contains", query)))
        return q


def payment_add(request, enrollment_id):
    obj = models.Enrollment.objects.filter(pk=enrollment_id).values("customer")
    for i in obj:
        ge = i['customer']
    obj = models.PaymentRecord(customer_id=ge)
    form_obj = form.PaymentForm(instance=obj)
    if request.method == "POST":
        form_obj = form.PaymentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse("payment_list"))
    return render(request, "froms.html", {"form_obj": form_obj, "title": "添加缴费信息"})


def payment_edit(request, payment_id):
    obj = models.PaymentRecord.objects.filter(pk=payment_id).first()
    form_obj = form.PaymentForm(instance=obj)
    if request.method == "POST":
        form_obj = form.PaymentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse("payment_list"))
    return render(request, "froms.html", {"form_obj": form_obj, "title": "修改缴费信息"})
