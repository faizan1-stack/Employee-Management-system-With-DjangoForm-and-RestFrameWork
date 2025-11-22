from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, Phone_number, password=None):
        if not email:
            raise ValueError('Please provide the email')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            Phone_number=Phone_number,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, Phone_number, password=None):
        user = self.create_user(
            username=username,
            email=email,
            Phone_number=Phone_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True  
        user.is_active = True
        user.save(using=self._db)
        return user
        
class User(PermissionsMixin,AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    Phone_number = models.CharField(max_length=15 , null=True , blank=True)
    role = models.CharField(max_length=20, default='employee')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username', 'Phone_number']

    def __str__(self):
        return f'{self.username}'


class EmployeeDetail(models.Model):
    emp_user = models.OneToOneField(settings.AUTH_USER_MODEL,   on_delete=models.CASCADE , related_name='emp_detail')
    emp_id = models.AutoField(primary_key=True)
    Department_Choices = [
        ('Manager' , 'Manager'),
        ('Frontend_Developer' , 'Frontend_Developer'),
        ('Backend_Developer' , 'Backend_Developer'),
        ('Fullstack_Developer' , 'Fullstack_Developer'),
        ('Designer' , 'Designer'),
        ('QA' , 'QA'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    Employee_Choices = [
        ('intern' , 'intern'),
        ('junior' , 'junior'),
        ('Associate' , 'Associate'),
        ('senior' , 'senior'),
        ('lead' , 'lead'),
        ('manager' , 'manager'),
    ]

    emp_address = models.TextField(max_length=300 , null=False , blank=False)
    emp_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    emp_department = models.CharField(choices=Department_Choices ,   max_length=20)
    emp_position = models.CharField(choices=Employee_Choices , null=False , blank=False)
    emp_hire_date = models.DateField(null=False , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f" {self.emp_department}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee Detail'
        verbose_name_plural = 'Employee Details'


class EmpAttendence(models.Model):
    employee = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"attendence of {self.employee.emp_user.username} - {self.date}" 

class LeaveRequest(models.Model):

    LeaveType=[
        ('Sick Leave' , 'Sick Leave'),
        ('Casual Leave' , 'Casual Leave'),
        ('Annual Leave' , 'Annual Leave'),
        ('Maternity Leave' , 'Maternity Leave'),
        ('Paternity Leave' , 'Paternity Leave'),
        ('Bereavement Leave' , 'Bereavement Leave'),
        ('Unpaid Leave' , 'Unpaid Leave')
    ]
    employee = models.ForeignKey(EmployeeDetail , on_delete=models.CASCADE , related_name='leave_requests')
    leave_type = models.CharField(max_length=20 ,choices=LeaveType  , null=True , blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=30 , null=True , blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    total_days = models.DecimalField(max_digits=20 , decimal_places=1 , default=0)
    used_days = models.DecimalField(max_digits=20 , decimal_places=1 , default=0)
    remaining_days = models.DecimalField(max_digits=20 , decimal_places=1 , default=0)

    def __str__(self):
        return f"Leave request of {self.employee.emp_user.username} - {self.leave_type}"
    
    def save(self ,*args , **kwargs):
        self.remaining_days = self.total_days - self.used_days
        super().save(*args , **kwargs)

class LeaveApproved(models.Model):
    Status_Choices = [
        ('Pending' , 'Pending'),
        ('Approved' , 'Approved'),
        ('Rejected' , 'Rejected')
    ]
    request_leave = models.OneToOneField(LeaveRequest , on_delete=models.SET_NULL , null=True, blank=True)
    status = models.CharField(choices=Status_Choices , max_length=20, default='Pending' )
    approved_by = models.ForeignKey(EmployeeDetail , on_delete=models.SET_NULL , null=True , blank=True , related_name='approved_leaves')
    reason = models.TextField(max_length=300 , null=True , blank=True)

    def __str__(self):
        return f"leave approve status{self.status} - {self.approved_by.emp_user.username}"

    '''
    def clean(self):
        super().clean()
        if self.approved_by.emp_position != 'manager':
            raise ValidationError(
                f"{self.approved_by.emp_user.username} does not have permission to approve this leave."
            )
    
    def save(self , *args , **kwargs):
        self.full_clean()
        super().save(*args , **kwargs)
 '''
        
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=25)
    project_description = models.TextField(max_length=300 , null=True , blank=True)
    project_lead = models.ForeignKey(EmployeeDetail , on_delete=models.SET_NULL , null=True , blank=True)
    project_member = models.ManyToManyField(EmployeeDetail , related_name='Project_Member' , blank=True)
    Project_Choice = [
        ('Active' , 'Active'),
        ('On_Hold' , 'On_Hold'),
        ('Completed' , 'Completed')
    ]
    project_status = models.CharField(choices=Project_Choice , null=False , blank=True)
    project_deadline = models.DateField(null=False , blank=False)
    project_document = models.FileField(upload_to='project_documents/' , null=True , blank=True)

    def clean(self):
        super().clean()
        if self.project_lead and self.project_lead.emp_position != 'manager':
            raise ValidationError({
                'project_lead': f'{self.project_lead.emp_user} is not eligible to be a project lead.'
            })
    def save(self , *args , **kwargs):
        self.full_clean()
        super().save(*args , **kwargs)

    def __str__(self):
        return f"{self.project_name}"

class Task(models.Model):
    task_name = models.CharField(max_length=150 , null=False , blank=True , verbose_name=_("Task Name"))
    task_description = models.TextField(max_length=300 ,null = False , blank = True , verbose_name=_("Task Description"))
    task_project = models.ForeignKey(Project , on_delete=models.CASCADE, related_name = 'task')
    created_by = models.ForeignKey(EmployeeDetail , on_delete=models.SET_NULL , null=True , blank=True , related_name='created_tasks', verbose_name=_("Created By"))
    assigned_to = models.ForeignKey(EmployeeDetail , on_delete=models.SET_NULL , null=True , blank=True , related_name='assigned_tasks' , verbose_name=_("Assigned To"))
    Task_Choice = [
        ('To_Do' , 'To_Do'),
        ('In_Progress' , 'In_Progress'),
        ('Completed' , 'Completed')
    ]
    Status = models.CharField(choices=Task_Choice , null=False , default='To_Do', blank=True , verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=False , blank=False)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ['due_date']

    def clean(self):
        super().clean()

        if not self.task_project_id or not self.assigned_to_id:
            return

        try:
            project = self.task_project
            emp = self.assigned_to

            is_lead = project.project_lead_id == emp.emp_id
            is_member = project.project_member.filter(emp_id=emp.emp_id).exists()

            if not (is_lead or is_member):
                raise ValidationError({
                    'assigned_to': _(
                        f'{emp.emp_user.username} is not a member '
                        f'of project "{project.project_name}"'
                    )
                })
        except (Project.DoesNotExist, EmployeeDetail.DoesNotExist):
            pass

    def __str__(self):
        return f"{self.task_name} - {self.task_project.project_name}"
        

    



# Create your models here.
