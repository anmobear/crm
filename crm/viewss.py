# import hashlib
# from django.http.request import QueryDict
# from django.shortcuts import render, redirect, reverse, HttpResponse
# from django.views import View
# from crm import form
# from crm import models
# from utils.pagination import Pagination
# from django.db.models import  Q
# def index(request):
#     return HttpResponse ( "dsahdkaslkdlaskjlkasjldjasd成功了 " )
#
#
# def login(request):
#     if request.method == "POST":
#         uname = request.POST.get ( "username" )
#         pwd = request.POST.get ( "password" )
#         md5 = hashlib.md5 ()    # md5加密
#         md5.update ( pwd.encode ( "utf-8" ) )
#         pwd = md5.hexdigest ()
#         obj = models.UserProfile.objects.filter ( username=uname, password=pwd, is_active=True ).first () # 验证密码
#         if obj:
#             request.session["u_id"] = obj.pk    # 添加session
#             return redirect ( reverse ( 'list' ) )
#         else:
#             return render ( request, "login.html", {"arror": "用户或密码输入错误!!!"} )
#     return render ( request, "login.html" )
#
# # 注册
# def reg(request):
#     if request.method == "POST":
#         form_obj = form.Forms ( request.POST )
#         # print ( form_obj.is_valid () )
#         if form_obj.is_valid ():   # 判断有没有 error
#             form_obj.save ()
#             return redirect ( reverse ( "login" ) )
#     else:
#         form_obj = form.Forms ()
#     return render ( request, "reg.html", {"from_obj": form_obj} )
# # 展示客户页面
# class CustomerList(View):
#     # get请求页面
#     def get(self,request):
#         query = request.GET
#         print ( query, type ( query ) )
#         q = self.search ( ["name", "qq"] )
#         if request.path_info == reverse("list"):
#             customer = models.Customer.objects.filter(q,consultant__isnull=True,) # 显示共户的内容
#         else:
#             customer = models.Customer.objects.filter (q,consultant=request.user_obj )
#         present_page = request.GET.get ( "page", "1" )  # 当前页数
#         pag = Pagination(present_page,len(customer), request.GET.copy(), 2)
#         # print(pag.page_num)
#         return render ( request, "customer_list.html", {"customer_obj": customer[pag.start:pag.end], "ret": pag.page_html} )
#     def post(self,request):
#         action =  request.POST.get("action")
#         # print(action)
#         if hasattr(self, action):
#             getattr(self, action)()
#         return self.get(request)
#
#     def multi_apply(self):
#         ids = self.request.POST.get("ids","")
#         models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)
#     def multi_pub(self):
#         ids = self.request.POST.get ( "ids","")
#         models.Customer.objects.filter ( pk__in=ids ).update ( consultant=None )
#
#     def search(self,field_list):
#         query = self.request.GET.get ( "query", "" )
#         q = Q()
#         q.connector = "OR"
#         for i in field_list:
#             # Q(Q(name__contains=query)|Q(qq__contains=query ))
#             # q.children.append(Q(('{}__contains'.format(i),query)))
#             q.children.append(Q((f"{i}__contains",query)))
#         return q
#
# # 显示内容
# # def customer_list(request):
# #     customer = models.Customer.objects.filter ( consultant__isnull=True )  # 显示共户的内容
# #     return render ( request, "customer_list.html", {"customer_obj": customer, } )
# #
# #
# # # 私户的
# # def my_customer(request):
# #     customer = models.Customer.objects.filter(consultant=request.user_obj)
# #     return render( request, "customer_list.html",{"customer_obj": customer, } )
#
#
# # def customer_add(request):
# #     form_obj =  form.AddForm()
# #     if request.method == "POST":
# #         form_obj = form.AddForm(request.POST)
# #         if form_obj.is_valid():
# #             form_obj.save()
# #             return redirect(reverse("list"))
# #     return render(request, "customer_add.html", {"form_obj": form_obj})
# #
# #
# # def customer_edit(request, edit_id=None):
# #     obj = models.Customer.objects.filter(pk=edit_id).first()
# #     from_obj = form.AddForm(instance=obj)
# #     if request.method == "POST":
# #         from_obj = form.AddForm(request.POST, instance=obj)
# #         if from_obj.is_valid():
# #             print(from_obj.is_valid())
# #             from_obj.save()
# #             return redirect(reverse("list"))
# #     return render(request, "customer_edit.html", {"form_obj": from_obj})
# # 编辑添加
# def customer_change(request, edit_id=None):
#     obj = models.Customer.objects.filter ( pk=edit_id ).first ()    # 取信息的对象
#     from_obj = form.AddForm ( instance=obj )
#     if request.method == "POST":
#         from_obj = form.AddForm ( request.POST, instance=obj )
#         if from_obj.is_valid ():
#             # print ( from_obj.is_valid () )
#             from_obj.save ()      # models 直接生成input标签
#             taxt = request.GET.get("url")
#             print(request.GET)
#             print(taxt)
#             return redirect (taxt )      # 重定向到 customer_list 页面里面
#     stutas =  "编辑客户" if edit_id else "添加客户"     # 用三元表达式你要判断的
#     return render ( request, "customer_edit.html", {"form_obj": from_obj, "stutas":stutas} )
#
# # def user_list(request):
# #
# #     present_page = request.GET.get("page","1")   # 当前页数
# #     # print(present_page)
# #     all_count = len(user_lst)      # 总数量
# #     pag = Pagination (present_page, all_count)
# #
# #     # every_page = 10                # 显示数量
# #     # page_count,odd = divmod(all_count, every_page)  # page_count 总页数
# #     # if odd:
# #     #     page_count += 1
# #     # try:
# #     #     present_page = int(present_page)
# #     #     if present_page <= 0:
# #     #         present_page = 1
# #     #     elif present_page > page_count:
# #     #         present_page = page_count
# #     # except Exception as e:
# #     #     present_page = 1
# #     #
# #     # max_show = 11
# #     # half_show = max_show // 2   # 中间
# #     # # if present_page
# #     # if present_page < half_show:
# #     #     start = 1
# #     #     end = max_show
# #     # else:
# #     #     if present_page <= half_show:
# #     #         start = 1
# #     #         end = max_show
# #     #     elif present_page+half_show >= page_count:
# #     #         start = page_count - max_show +1
# #     #         end = page_count
# #     #     else:
# #     #         start = present_page - half_show
# #     #         end = present_page + half_show
# #     #
# #     # page_list = []
# #     # if present_page == 1:
# #     #     page_list.append ( f'<li class="hidden">上一页</li>' )
# #     # else:
# #     #     page_list.append ( f'<li ><a href="?page={present_page-1}">上一页</a></li>' )
# #     # for i in range(start, end +1 ):
# #     #     if i == present_page:
# #     #         page_list.append ( '<li class="active"><a href="?page={}">{}</a></li>'.format ( i, i ) )
# #     #     else:
# #     #         page_list.append ( '<li><a href="?page={}">{}</a></li>'.format ( i, i ) )
# #     #
# #     # if present_page == page_count:
# #     #     page_list.append ( f'<li class="hidden">上一页</li>' )
# #     # else:
# #     #     page_list.append ( f'<li ><a href="?page={present_page + 1}">下一页</a></li>' )
# #     #
# #     # ret = "".join(page_list)
# #     # print(ret)
# #
# #     # print(pag.start, pag.end)
# #     return render ( request, "user_list.html", {"user_list": user_lst[pag.start:pag.end],
# #                                                 "ret": pag.page_html})
#
#
#
#
