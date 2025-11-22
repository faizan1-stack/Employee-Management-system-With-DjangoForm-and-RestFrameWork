from django.contrib import admin
from empcrud.models import LeaveRequest, LeaveApproved
# Register your models here.
admin.site.register(LeaveRequest)
admin.site.register(LeaveApproved)
