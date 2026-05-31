from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_role', 'ctc', 'eligibility_cgpa', 'allowed_branches', 'drive_notice')
    search_fields = ('company_name', 'job_role')
    list_filter = ('allowed_branches', 'drive_notice')


admin.site.register(Student)
admin.site.register(application)
admin.site.register(MockTest)
admin.site.register(Question)
admin.site.register(StudentAnswer)