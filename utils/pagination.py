#
from django.http.request import QueryDict
#
# class Pagination:
#
#     def __init__(self, present_page, all_count, every_page=10, max_show=11):
#         try:
#             self.present_page = int ( present_page )
#             if self.present_page <= 0:
#                 self.present_page = 1
#             # elif self.present_page > self.page_count:
#             #    self.present_page = self.page_count
#         except Exception as e:
#
#             self.present_page = 1
#         print(self.present_page)
#         # if present_page
#         self.every_page = every_page
#         self.page_count, odd = divmod ( all_count, every_page )  # page_count 总页数
#         if odd:
#             self.page_count += 1
#         self.max_show = max_show
#         self.half_show = max_show // 2  # 中间
#
#     @property
#     def page_html(self):
#         if self.present_page < self.half_show:
#             start = 1
#             end = self.max_show
#         else:
#             if self.present_page <= self.half_show:
#                 start = 1
#                 end = max_show
#             elif self.present_page + self.half_show >= self.page_count:
#                 start = self.page_count - self.max_show + 1
#                 end = self.page_count
#             else:
#                 start = self.present_page - self.half_show
#                 end = self.present_page + self.half_show
#         page_list = []
#         if self.present_page == 1:
#             page_list.append("<li class='disabled'><a> 上一页</a></li>")
#         else:
#             page_list.append ( '<li><a href="?page={}">上一页</a></li>'.format ( self.present_page - 1, ) )
#         for i in range ( start, end + 1 ):
#             if i == self.present_page:
#                 page_list.append ( '<li class="active"><a href="?page={}">{}</a></li>'.format ( i, i) )
#             else:
#                 page_list.append ( '<li><a href="?page={}">{}</a></li>'.format ( i, i) )
#         if self.present_page == self.page_count:
#             page_list.append ( '<li class="disabled"><a>下一页</a></li>')
#         else:
#             page_list.append(f'<li><a href="?page={self.present_page+1}"> 下一页</a></li> ')
#         # print(page_list)
#         return "".join(page_list)
#
#
#     @property
#     def start(self):
#         return (self.present_page-1) * self.every_page
#
#     @property
#     def end(self):
#         return self.present_page * self.every_page
#
class Pagination:
    def __init__(self, page_num, all_count, params=QueryDict(mutable=True),per_num=10, max_show=11):
        self.params = params
        # if self.params:
        #     self.params = QueryDict(mutable=True)
        #
        # print(">>>>>>>>>>",self.params.urlencode())
        # 获取页码
        try:
            self.page_num = int(page_num)
            if self.page_num <= 0:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1

        # 每页显示的数据量
        self.per_num = per_num

        # 总数据量
        all_count = all_count

        # 总页码数
        self.page_count, more = divmod(all_count, per_num)
        if more:
            self.page_count += 1

        # 最大显示页码数
        self.max_show = max_show
        self.half_show = max_show // 2


    @property
    def page_html(self):
        # 总页码数 < 最大显示页码数
        if self.page_count < self.max_show:
            page_start = 1
            page_end = self.page_count
        else:
            # 处理左边极值
            if self.page_num <= self.half_show:
                page_start = 1
                page_end = self.max_show
            elif self.page_num + self.half_show >= self.page_count:
                page_start = self.page_count - self.max_show + 1
                page_end = self.page_count
            else:
                page_start = self.page_num - self.half_show  # 2
                page_end = self.page_num + self.half_show  # 7 + 5  12

        page_list = []
        if self.page_num == 1:
            page_list.append('<li style="visibility:hidden" class="disabled"><a>上一页</a></li>')
        else:
            self.params["page"] = self.page_num - 1
            page_list.append('<li><a href="?{}">上一页</a></li>'.format(self.params.urlencode(), ))

        for i in range(page_start, page_end + 1):
            if i == self.page_num:
                page_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                self.params["page"] = i
                page_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))

        if self.page_num == self.page_count:
            page_list.append('<li style="visibility:hidden" class="disabled"><a>下一页</a></li>')
        else:
            self.params["page"] = self.page_num + 1
            page_list.append('<li><a href="?{}">下一页</a></li>'.format(self.params.urlencode(), ))
        return ''.join(page_list)

    @property
    def start(self):
        """
        切片的起始值
        :return:
        """
        return (self.page_num - 1) * self.per_num

    @property
    def end(self):
        """
        切片的终止值
        :return:
        """
        return self.page_num * self.per_num
