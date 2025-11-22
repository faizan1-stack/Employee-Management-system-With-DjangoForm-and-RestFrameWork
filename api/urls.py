from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('create-emp/', CreateEmp.as_view(), name='create-emp'),
    path('employee-detail/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee-detail/<int:emp_id>/', PerEmpDetailView.as_view(), name='per-employee-detail'), 
    path('delete-emp/<int:emp_id>/', DeleteEmpView.as_view(), name='delete-emp'), 
    path('Update_emp/<int:emp_id>/', UpdateEmpView.as_view(), name='update-emp'),
    path('Attendence_checkin/<int:emp_id>/', EmpAttendenceCheckInView.as_view(), name='attendence-checkin'),
    path('Attendence_checkout/<int:emp_id>/', EmpAttendenceCheckOutView.as_view(), name='attendence-checkout'),
    path('Emp_Attendence_Report/<int:emp_id>/', EmpAttendenceReport.as_view(), name='emp-attendence-report'),
    path('leave_request/<int:emp_id>/', LeaveRequestView.as_view(), name='leave-request'),
    path('leave_approve/<int:leave_id>/', LeaveApprovedView.as_view(), name='leave-approve'),
    path('Leave-approve/<int:emp_id>/' , LeaveApprovedView.as_view() , name='Leave-approve' )

]
