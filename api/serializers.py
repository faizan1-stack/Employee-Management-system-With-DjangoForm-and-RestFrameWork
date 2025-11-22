from rest_framework import serializers
from empcrud.models import User, EmployeeDetail, Project, Task , EmpAttendence , LeaveRequest , LeaveApproved
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs
    

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username' , 'email' , 'password', 'Phone_number' ]
        extra_kwargs = {
            'password' :{'write_only' : True},
            'username': {'required': True},
            'Phone_number': {'required': True}
        }
        def create(self , validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                Phone_number=validated_data['Phone_number'],
                password=validated_data['password']
            )
            return user


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetail
        fields = [
            'emp_id',
            'emp_user',
            'emp_address',
            'emp_gender',
            'emp_department',   
            'emp_position',
            'emp_hire_date',
        ]
        extra_kwargs = {
            'emp_user': {'read_only': True},
            'emp_id' : {'read_only' : True}
        }

class EmpAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpAttendence
        fields = [
            'employee',
            'date',
            'check_in',
            'check_out',
            'status',
        ]
        extra_kwargs = {
        }



class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'employee',
            'reason',
            'leave_type',
            'start_date',
            'end_date',
        ]
        extra_kwargs = {
          'reason': {'read_only' : True}
        }

class LeaveApprovedSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'status',
            'rejection_reason',
        ]
        extra_kwargs = {
            'status': {'required': True},
        }

class LeaveApprovedSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveApproved
        fields = [
           'request_leave',
            'status' ,
            'reason',
            'approved_by'
        ]
    def validate(self ,attrs):
        request_leave = attrs.get('request_leave')
        if LeaveApproved.objects.filter(request_leave=request_leave).exists():
            return serializers.ValidationError({'message' : 'this leave is already approved or rejected'})
            
        return attrs