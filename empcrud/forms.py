from django import forms
from .models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password',
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'Phone_number', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),   
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetail
        exclude = ('emp_user',) 
        widgets = {
            'emp_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_address': forms.Textarea(attrs={'class': 'form-control'}),
            'emp_gender': forms.Select(attrs={'class': 'form-control'}),
            'emp_department': forms.Select(attrs={'class': 'form-control'}),
            'emp_position': forms.Select(attrs={'class': 'form-control'}),
            'emp_hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'emp_contact': 'Phone Number',
            'emp_department': 'Department',
            'emp_position': 'Position',
            'emp_gender': 'Gender',
            'emp_address': 'Address',
            'emp_hire_date': 'Hire Date',
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name' , 'project_description' , 'project_lead' , 'project_member' , 'project_status' , 'project_deadline' , 'project_document']
        widgets = {
            'project_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'project_description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'project_lead' : forms.Select(attrs={'class' : 'form-control'}),
            'project_member' : forms.SelectMultiple(attrs={'class' : 'form-control'}),
            'project_status' : forms.Select(attrs={'class' : 'form-control'}),
            'project_deadline' : forms.DateInput(attrs={'class' : 'form-control', 'type': 'date'}),
            'project_document' : forms.FileInput(attrs={'class' : 'form-control'}),
            }
        
        labels = {
            'project_name' : 'Project Name',
            'project_description' : 'Project Description',
            'project_lead' : 'Project Lead',
            'project_member' : 'Project Members',
            'project_status' : 'Project Status',
            'project_deadline' : 'Project Deadline',
            'project_document' : 'Project Document',

        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'task_project', 'created_by', 'assigned_to', 'Status', 'due_date']
        widgets = {
            'task_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'task_description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'task_project' : forms.Select(attrs={'class' : 'form-control'}),
            'created_by' : forms.Select(attrs={'class' : 'form-control'}),
            'assigned_to' : forms.Select(attrs={'class' : 'form-control'}),
            'Status' : forms.Select(attrs={'class' : 'form-control'}),
            'due_date' : forms.DateInput(attrs={'class' : 'form-control', 'type': 'date'}),
        }
        labels = {
            'task_name' : 'Task Name',
            'task_description' : 'Task Description',
            'task_project' : 'Task Project',
            'created_by' : 'Created By',
            'assigned_to' : 'Assigned To',
            'Status' : 'Task Status',
            'due_date' : 'Due Date',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize assigned_to with all employees
        self.fields['assigned_to'].queryset = EmployeeDetail.objects.all()
        
        if 'task_project' in self.data:
            try:
                project_id = int(self.data.get('task_project'))
                self.fields['assigned_to'].queryset = self.get_project_members(project_id)
            except (ValueError, TypeError):
                self.fields['assigned_to'].queryset = EmployeeDetail.objects.all()
        elif self.instance.pk and self.instance.task_project_id:
            # If editing existing task, show members of that project
            self.fields['assigned_to'].queryset = self.get_project_members(
                self.instance.task_project_id
            )
    
    def get_project_members(self, project_id):
        """Get all valid members for a project (lead + members)"""
        try:
            project = Project.objects.get(pk=project_id)
            members = project.project_member.all()
            lead = EmployeeDetail.objects.filter(emp_id=project.project_lead_id)
            return (members | lead).distinct()
        except Project.DoesNotExist:
            return EmployeeDetail.objects.all()
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        project = cleaned_data.get('task_project')
        assigned_to = cleaned_data.get('assigned_to')
        
        # Only validate if both fields are present
        if project and assigned_to:
            is_lead = project.project_lead_id == assigned_to.emp_id
            is_member = project.project_member.filter(emp_id=assigned_to.emp_id).exists()
            
            if not (is_lead or is_member):
                raise forms.ValidationError({
                    'assigned_to': f'{assigned_to.emp_user.username} is not a member of project "{project.project_name}"'
                })
        
        return cleaned_data
    