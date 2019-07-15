from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from crm import form
from crm import models
from utils.pagination import Pagination


class EnrollmentList(View):

    def get(self, request, *args, **kwargs):
        query = request.GET
        q = self.search([])
        enrollment = models.Enrollment.objects.filter(q, customer__consultant=request.user_obj, delete_status=False)

        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(enrollment), request.GET.copy(), 2)
        # print(pag.page_num)
        return render(request, "customer/enrollment_list.html",
                      {"enrollment_obj": enrollment[pag.start:pag.end], "ret": pag.page_html})

    def search(self, field_list):
        query = self.request.GET.get("query", "")
        q = Q()
        q.connector = "OR"
        for i in field_list:
            # Q(Q(name__contains=query)|Q(qq__contains=query ))
            # q.children.append(Q(('{}__contains'.format(i),query)))
            q.children.append(Q((f"{i}__contains", query)))
        return q


def enrollment_change(request, customer_id=None, enrollment_id=None):
    # obj = models.Enrollment(customer_id=customer_id)
    #
    # obj = models.Enrollment.objects.filter(pk=enrollment_id)

    obj = models.Enrollment(customer_id=customer_id) if customer_id else models.Enrollment.objects.filter(
        pk=enrollment_id).first()
    title = '新增报名' if customer_id else '编辑报名'
    form_obj = form.EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = form.EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            # next = request.GET.get('next')
            next = request.GET.get("next")
            return redirect(next)
    return render(request, 'froms.html', {'form_obj': form_obj, "title": title})
