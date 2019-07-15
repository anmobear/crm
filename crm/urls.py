from django.conf.urls import url, include
from django.contrib import admin
from crm.views import auth, customer, consult, enrollment, payment, class_

urlpatterns = [
    url(r"^login/", auth.login, name="login"),
    url(r"^index/", auth.index, name="index"),
    url(r"^reg/", auth.reg, name="reg"),
    url(r"^list/", customer.CustomerList.as_view(), name="list"),
    # url(r"^user_list/", views.user_list, name="user_list"),
    # 添加客户
    url(r"^customer_add/", customer.customer_change, name="customer_add"),
    # 显示自己的客户
    url(r"^my_customer/", customer.CustomerList.as_view(), name="my_customer"),
    # 更改客户
    url(r"^customer_edit/(\d+)$", customer.customer_change, name="customer_edit"),

    # 展示跟进
    url(r"^consult_list/$", consult.ConsultList.as_view(), name="consult_list"),
    url(r"^consult_list/(?P<customer_id>\d+)", consult.ConsultList.as_view(), name="one_consult"),
    url(r"^consult_add/", consult.consult_change, name="consult_add"),
    url(r"^consult_edit/(\d+)$", consult.consult_change, name="consult_edit"),

    # 报名
    url(r"^enrollment_list/$", enrollment.EnrollmentList.as_view(), name="enrollment_list"),
    # url ( r"^enrollment_list/$", enrollment.EnrollmentList.as_view (), name="one_enrollment" ),
    url(r"^enrollment_add/(?P<customer_id>\d+)", enrollment.enrollment_change, name="enrollment_add"),
    url(r"^enrollment_edit/(?P<enrollment_id>\d+)", enrollment.enrollment_change, name="enrollment_edit"),
    # url ( r"^enrollment_edit/(\d+)$", enrollment.enrollment_edit, name="enrollment_edit" ),

    # 缴费
    url(r"payment_list/$", payment.PaymentList.as_view(), name="payment_list"),
    # url ( r"^enrollment_list/$", enrollment.EnrollmentList.as_view (), name="one_enrollment" ),
    url(r"^payment_add/(?P<enrollment_id>\d+)", payment.payment_add, name="payment_add"),
    url(r"^payment_edit/(?P<payment_id>\d+)", payment.payment_edit, name="payment_edit"),

    #  班级管理
    url(r"^class_list/$", class_.ClassList.as_view(), name="class_list"),
    url(r"^class_add/$", class_.class_change, name="class_add"),
    url(r"^class_edit/(?P<class_id>\d+)", class_.class_change, name="class_edit"),
    # 课程记录
    url(r"^course_record_list/(?P<class_id>\d+)$", class_.CourseRecordList.as_view(), name="course_record_list"),
    url(r"^course_record_add/(?P<class_id>\d+)$", class_.course_record_change, name="course_record_add"),
    url(r"^course_record_edit/(?P<course_id>\d+)$", class_.course_record_change, name="course_record_edit"),

    url(r'^study_record_list/(?P<course_record_id>\d+)/$', class_.study_record_list, name='study_record_list'),
    # 学习记录的初始化
    # url ( r"^course_record_edit/(?P<course_id>\d+)$", class_.course_record_change, name="course_record_edit"),
]
