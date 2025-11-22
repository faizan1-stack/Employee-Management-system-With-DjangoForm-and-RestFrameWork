from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .renderer import UserRenderer
from django.db import transaction
from empcrud.models import EmployeeDetail,  LeaveRequest, LeaveApproved
from django.db.models import Q
from .premissions import IsAdminUser , IsEmployeeUser
from datetime import datetime, date

class UserLogin(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    def post(self , request , *args ,**kwargs):
      serializers = LoginSerializer(data = request.data)
      if serializers.is_valid(raise_exception=True):
         email = serializers.validated_data.get('email')
         password = serializers.validated_data.get('password')
         user = authenticate(request ,email=email , password=password)
         if user is None:
            return Response({'error' : 'Invalid email or password'} , status = status.HTTP_401_UNAUTHORIZED)
         return Response({'message' : 'Login Successful'} , status = status.HTTP_200_OK)
      return Response(serializers.errors , status = status.HTTP_400_BAD_REQUEST)


class CreateEmp(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , *args, **kwargs):
        user_serializer = UserSerializer(data = request.data)
        emp_serilaizer = EmployeeSerializers(data = request.data)
        if user_serializer.is_valid() and emp_serilaizer.is_valid():
           try:
              with transaction.atomic():
                 user = user_serializer.save()
                 emp_serilaizer.save(emp_user=user)
                 return Response({'message' : 'Employee created successfully'} , status = status.HTTP_201_CREATED)
           except Exception as e:
              return Response({'error' : str(e)} , status= status.HTTP_400_BAD_REQUEST)
        else:
           errors = {}
           errors.update(user_serializer.errors)
           errors.update(emp_serilaizer.errors)
           return Response(errors , status= status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated , IsAdminUser]
    def get(self, request, *args, **kwargs):
        emp_user = EmployeeDetail.objects.all()
        search = request.GET.get('search')
        if search:
            emp_user = emp_user.filter(
                Q(emp_user__username__icontains=search) |
                Q(emp_department__icontains=search.replace(" ", "_")) |
                Q(emp_position__icontains=search)
            )


        department = request.GET.get('department')
        if department:
            dept_clean = department.replace(" ", "_").capitalize()
            emp_user = emp_user.filter(emp_department__icontains=dept_clean)

        emp_position = request.GET.get('position')
        if emp_position:
            emp_user = emp_user.filter(emp_position__icontains=emp_position.lower())


        gender = request.GET.get('gender')
        if gender:
            gender = gender[0].upper()  
            emp_user = emp_user.filter(emp_gender=gender)

        return Response(
            {"employees": EmployeeSerializers(emp_user, many=True).data},
            status=status.HTTP_200_OK
        )


class PerEmpDetailView(APIView):
   renderer_classes = [UserRenderer]
   permission_classes = [IsAuthenticated , IsEmployeeUser]
   def get(self , request , emp_id , *args, **kwargs):
      emp_id = EmployeeDetail.objects.get(emp_id=emp_id)
      if request.user.is_authenticated and request.user.role=='employee' and   request.user !=emp_id.emp_user:
         return Response({'error': 'You are not authorized to view this employee details'}, status=status.HTTP_403_FORBIDDEN)
      return Response({'employee' : EmployeeSerializers(emp_id).data} , status = status.HTTP_200_OK)


class DeleteEmpView(APIView):
   renderer_classes = [UserRenderer]
   def delete(self , request , emp_id , *args , **kwargs):
      emp_id = EmployeeDetail.objects.get(emp_id=emp_id)
      emp_id.delete()
      return Response({'message' : 'Employee deleted successfully'} , status = status.HTTP_200_OK)
   


class UpdateEmpView(APIView):
   renderer_classes = [UserRenderer]
   def put (self , request , emp_id , *args , **kwargs):
      emp_id = EmployeeDetail.objects.get(emp_id = emp_id)
      form = EmployeeSerializers(emp_id , data = request.data , partial = True) 
      if form.is_valid():
         form.save()
         return Response({'message' : 'Employee updated successfully'} , status = status.HTTP_200_OK)
      return Response(form.errors , status = status.HTTP_400_BAD_REQUEST)  


class EmpAttendenceCheckInView(APIView):
   renderer_classes = [UserRenderer]
   permission_classes =[IsAdminUser | IsEmployeeUser]
   def post (self , request , emp_id, *args , **kwargs):
      try:
         emp = EmployeeDetail.objects.get(emp_id=emp_id)
      except EmployeeDetail.DoesNotExist:
         return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND) 
      if request.user.is_authenticated and request.user.role=='employee' and   request.user !=emp.emp_user:
         return Response({'error': 'You are not authorized to check in for this employee'}, status=status.HTTP_403_FORBIDDEN)

      today = date.today()
      attendence , created = EmpAttendence.objects.get_or_create(
         employee=emp ,
         date = today)
      
      if attendence.check_in is not None:
         return Response({'error': 'Check-in already recorded for today'}, status=status.HTTP_400_BAD_REQUEST)
      
      attendence.check_in = datetime.now().time()
      attendence.save()
      return Response({'message': 'Check-in recorded successfully'}, status=status.HTTP_200_OK)
   

class EmpAttendenceCheckOutView(APIView):
   renderer_classes = [UserRenderer]
   permission_classes =[IsAdminUser | IsEmployeeUser]
   def post (self , request , emp_id, *args , **kwargs):
      try:
         emp = EmployeeDetail.objects.get(emp_id=emp_id)
      except EmployeeDetail.DoesNotExist:
         return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND) 
      if request.user.is_authenticated and request.user.role=='employee' and   request.user !=emp.emp_user:
         return Response({'error': 'You are not authorized to check out for this employee'}, status=status.HTTP_403_FORBIDDEN)

      today = date.today()
      try:
         attendence = EmpAttendence.objects.get(
            employee=emp ,
            date = today)
      except EmpAttendence.DoesNotExist:
         return Response({'error': 'Check-in not recorded for today'}, status=status.HTTP_400_BAD_REQUEST)
      
      if attendence.check_out is not None:
         return Response({'error': 'Check-out already recorded for today'}, status=status.HTTP_400_BAD_REQUEST)
      
      attendence.check_out = datetime.now().time()
      attendence.save()
      return Response({'message': 'Check-out recorded successfully'}, status=status.HTTP_200_OK)

class EmpAttendenceReport(APIView):
    renderer_classes = [UserRenderer]
    permission_classes =[IsAdminUser]
    def get(self , request , emp_id , *args , **kwargs):
       try:
          emp = EmployeeDetail.objects.get(emp_id=emp_id)
       except EmployeeDetail.DoesNotExist:
          return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
       record = EmpAttendence.objects.filter(
          employee = emp,   
       )
       serializer = EmpAttendenceSerializer(record , many=True)
       return Response({'attendence_record' : serializer.data} , status = status.HTTP_200_OK)


class LeaveRequestView(APIView):
   renderer_classes = [UserRenderer]
   def post(self ,request ,emp_id, *args , **kwargs):
      
      try:
         emp = EmployeeDetail.objects.get(emp_id = emp_id)
      except EmployeeDetail.DoesNotExist:
         return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
      
      serializer = LeaveRequestSerializer(data=request.data)

      if not serializer.is_valid():
         return Response(serializer.error , status=status.HTTP_400_BAD_REQUEST)
      
      start_date = serializer.validated_data.get('start_date')
      end_date = serializer.validated_data.get('end_date')
      leave_request = LeaveRequest.objects.filter(
            employee=emp , 
            start_date__lte=end_date ,
            end_date__gte=start_date
        ).exists()
      
      if leave_request:
          return Response({'message': 'Leave request Already Submitted'}, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save(employee=emp)
      return Response({'message': 'Leave request submitted successfully'}, status=status.HTTP_201_CREATED)


class LeaveApprovedView(APIView):
   renderer_classes = [UserRenderer]
   def post(self , request , emp_id , *args , **kwargs):
      try:
         emp = EmployeeDetail.objects.get(emp_id=emp_id)
      except EmployeeDetail.DoesNotExist:
         return Response({'message' : 'Employe does not exists'} , status=status.HTTP_404_NOT_FOUND)
      
      leave_id = (
         request.data.get('request_leave')
         or request.data.get('leave_id')
         or request.query_params.get('request_leave')
         or request.query_params.get('leave_id')
      )
      if not leave_id:
         return Response({'message': 'request_leave is required'}, status=status.HTTP_400_BAD_REQUEST)

      try:
          leave_request = LeaveRequest.objects.get(id = leave_id)
      except LeaveRequest.DoesNotExist:
         return Response({'message' : 'Leave Request does not exist'}, status=status.HTTP_404_NOT_FOUND)
      
      if LeaveApproved.objects.filter(request_leave = leave_request).exists():
         return Response(
                {"message": "This leave request has already been approved or rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )

      overlapping_leave = LeaveRequest.objects.filter(
         employee=leave_request.employee,
         start_date__lte=leave_request.end_date,
         end_date__gte=leave_request.start_date,
         leaveapproved__status='Approved'
      ).exclude(id=leave_request.id).exists()

      if overlapping_leave:
         return Response(
            {"message": "Employee already has an approved leave for these dates."},
            status=status.HTTP_400_BAD_REQUEST
         )

      data = request.data.copy()
      data["approved_by"] = emp.emp_id
      data["request_leave"] = leave_request.id

      serializer = LeaveApprovedSerializers(data=data)
      if serializer.is_valid():
         approved_status = serializer.save()
         return Response({'message' : f"{approved_status.status}" }, status=status.HTTP_202_ACCEPTED)
      return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

      
      