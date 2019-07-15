from django.core.validators import ValidationError
from django import forms
from crm import models
import hashlib
# 注册,客户,私户
class Boot(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super ().__init__ ( *args, **kwargs )
        # print(self.fields)
        for field in self.fields.values ():
            if not isinstance(field,forms.BooleanField):
                field.widget.attrs.update ( {"class": "form-control"} )

class Forms(Boot):
    password = forms.CharField(widget=forms.PasswordInput, label="密码", min_length=6)
    re_password = forms.CharField(widget=forms.PasswordInput, label="确认密码", min_length=6)
    class Meta:
        model = models.UserProfile
        fields = "__all__"
        exclude = ["is_active","memo"]   # 排除
        required ={
            "username":True,
            "password":True,
            "re_password":True,
        }

        error_messages = {
            "username":{"required": "您输入的不能为空",
            "min_length": "长度不能小于6位", }}
        # widgets = {
            # 'username': forms.TextInput ( attrs={'class': 'form-control', 'placeholder': '用户名'} ),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'})
        # }

    def clean(self):
        pwd = self.cleaned_data.get("password","")
        re_pwd = self.cleaned_data.get("re_password","")
        # print(self.cleaned_data)
        # print(re_pwd, pwd)
        if pwd == re_pwd :
            md5 = hashlib.md5()
            md5.update(pwd.encode("utf-8"))
            pwd = md5.hexdigest()
            self.cleaned_data["password"] = pwd
            return self.cleaned_data
        self.add_error("re_password", "两次密码不一致请核对后再点!")
        raise ValidationError
    # labes = {
    #     "username": "账号",
    #     "mobile": "电话",
    #     "name": "姓名",
    #     "department":"部门"
    # }

class AddForm(Boot):
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super ().__init__ ( *args, **kwargs )
        self.fields['course'].widget.attrs.pop ( 'class' )

# 跟进的
class ConsultForm(Boot):
    class Meta:
        model = models.ConsultRecord
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(list(self.fields['customer'].choices))  # 可以选择的
        # print(self.instance.consultant)  # 当前的销售
        self.fields['customer'].choices = [(i.pk, str(i))for i in self.instance.consultant.customers.all()]
        # print(self.instance.consultant_id)
        self.fields['consultant'].choices = [(self.instance.consultant_id ,self.instance.consultant )]

# 报名的
class EnrollmentForm(Boot):
    class Meta:
        model  = models.Enrollment
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['customer'].choices =[(self.instance.customer_id,self.instance.customer)]
        self.fields['enrolment_class'].choices = [(i.pk, str ( i )) for i in self.instance.customer.class_list.all ()]

# 缴费的
class PaymentForm(Boot):
    class Meta:
        model = models.PaymentRecord
        fields = "__all__"

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        # print(self.instance.)
        # self.fields["course"].choices = []
        # print(">>>",self.instance.customer)
        self.fields['customer'].choices =[(self.instance.customer_id,self.instance.customer)]
        self.fields['consultant'].choices =[(self.instance.customer.consultant_id,self.instance.customer.consultant)]
        # self.fields['enrolment_class'].choices =[(self.instance.customer.class_list.all,self.instance.customer.class_list)]
        # print(self.instance.consultant)

# 班级的
class ClassForm(Boot):
    class Meta:
        model = models.ClassList
        fields = "__all__"

# 课程
class CourseRecordForm(Boot):
    class Meta:
        model = models.CourseRecord
        fields = "__all__"

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_class"].choices = [(self.instance.re_class_id,self.instance.re_class)]
        self.fields["teacher"].choices = [(self.instance.teacher_id,self.instance.teacher)]
class StudyRecordForm(Boot):
    class Meta:
        model = models.CourseRecord
        fields = "__all__"
    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)





