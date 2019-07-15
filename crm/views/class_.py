from django.http.request import QueryDict
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from crm import form
from crm import models
from utils.pagination import Pagination
from django.db.models import Q
from django.forms import modelformset_factory


# 显示班级
class ClassList(View):

    def get(self, request):
        model = models.ClassList.objects.all()
        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(model), request.GET.copy(), 2)
        return render(request, "teacher/class_list.html", {"class_obj": model[pag.start:pag.end], "ret": pag.page_html})


# 班级添加修改
def class_change(request, class_id=None):
    # from_obj = models.ClassList()
    if class_id:
        obj = models.ClassList.objects.filter(pk=class_id).first()
    else:
        obj = models.ClassList()
    form_obj = form.ClassForm(instance=obj)
    title = "编辑班级信息" if class_id else "添加班级信息"
    if request.method == "POST":
        form_obj = form.ClassForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get("next")
            print(next)
            return redirect(next)
    return render(request, "froms.html", {"form_obj": form_obj, "title": title})


class CourseRecordList(View):
    # 课程管理展示
    def get(self, request, class_id, *args, **kwargs):

        coutse_record = models.CourseRecord.objects.filter(re_class_id=class_id)

        present_page = request.GET.get("page", "1")  # 当前页数
        pag = Pagination(present_page, len(coutse_record), request.GET.copy(), 2)

        return render(request, "teacher/course_record_list.html", {
            'class_id': class_id
            , "course_record_obj": coutse_record[pag.start:pag.end], "ret": pag.page_html})

    def post(self, request, *args, **kwargs):

        action = request.POST.get("action")
        # print(action)
        if hasattr(self, action):
            ret = getattr(self, action)()
            if ret:
                return ret
        else:
            return HttpResponse("非法操作")
        return self.get(request, *args, **kwargs)

    def multi_init(self):

        course_record_ids = self.request.POST.getlist("ids")  # 拿取选中的id
        for course_record_id in course_record_ids:  # 是个列表 循环他取出一个
            course_record_obj = models.CourseRecord.objects.filter(pk=course_record_id).first()
            all_students = course_record_obj.re_class.customer_set.all().filter(status="studying")  # 取到所有的学生
            study_record_list = []
            for student in all_students:
                if models.StudyRecord.objects.filter(student=student, course_record_id=course_record_id).exists():
                    continue
                obj = models.StudyRecord(student=student, course_record_id=course_record_id)

                study_record_list.append(obj)

            print(study_record_list)
            models.StudyRecord.objects.bulk_create(study_record_list)


def course_record_change(request, class_id=None, course_id=None):
    obj = models.CourseRecord(re_class_id=class_id, teacher=request.user_obj) if class_id else models. \
        CourseRecord.objects.filter(pk=course_id).first()
    form_obj = form.CourseRecordForm(instance=obj)
    if request.method == "POST":
        form_obj = form.CourseRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get("next")
            if not next:
                next = reverse('course_record_list', class_id)
            return redirect(next)
    return render(request, "froms.html", {'form_obj': form_obj})


def study_record_list(request, course_record_id):
    Formset = modelformset_factory(models.StudyRecord, form.StudyRecordForm, extra=0)
    formset = Formset(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
    if request.method == "POST":
        formset = Formset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('study_record_list', args=(course_record_id,)))
    return render(request, 'teacher/study_record_list.html', {'formset': formset})
