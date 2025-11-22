from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeDetail , User


admin.site.register(User)

@admin.register(EmployeeDetail)
class EmployeeDetailAdmin(admin.ModelAdmin):
    list_display = ( 'emp_id'  , 'emp_department' , 'emp_position' )
    search_fields = ( 'emp_department' , 'emp_position' )
    list_filter = ('emp_department' , 'emp_position' )
    ordering = ('emp_id',)

