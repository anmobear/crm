from django.contrib import admin
from crm import models
admin.site.register(models.Customer)
# Register your models here.
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.CourseRecord)






