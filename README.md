# Employee Management System

A comprehensive Employee Management System built with Django and Django REST Framework. This system provides both web-based forms and RESTful API endpoints for managing employees, attendance, leave requests, projects, and tasks.

## Features

- **Employee Management**: Create, read, update, and delete employee records
- **Attendance Tracking**: Check-in and check-out functionality with attendance reports
- **Leave Management**: Submit leave requests and approve/reject them with overlap prevention
- **Project & Task Management**: Create projects, assign tasks, and track their status
- **Authentication**: User authentication with role-based access control (Admin/Employee)
- **RESTful API**: Complete API endpoints for all operations
- **Django Forms**: Web-based interface for employee management

## Technology Stack

- **Backend**: Django 5.2.6
- **API**: Django REST Framework 3.16.1
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Python**: 3.x

## Installation

### Prerequisites

- Python 3.x
- pip
- virtualenv (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/faizan1-stack/Employee-Management-system-With-DjangoForm-and-RestFrameWork.git
   cd Employee-Management-system-With-DjangoForm-and-RestFrameWork/emp
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The server will start at `http://127.0.0.1:8000/`

## API Endpoints

All API endpoints are prefixed with `/api-auth/`

### Authentication
- `POST /api-auth/login/` - User login

### Employee Management
- `POST /api-auth/create-emp/` - Create new employee
- `GET /api-auth/employee-detail/` - List all employees (with search, filter by department, position, gender)
- `GET /api-auth/employee-detail/<emp_id>/` - Get specific employee details
- `PUT /api-auth/Update_emp/<emp_id>/` - Update employee information
- `DELETE /api-auth/delete-emp/<emp_id>/` - Delete employee

### Attendance
- `POST /api-auth/Attendence_checkin/<emp_id>/` - Employee check-in
- `POST /api-auth/Attendence_checkout/<emp_id>/` - Employee check-out
- `GET /api-auth/Emp_Attendence_Report/<emp_id>/` - Get attendance report for employee

### Leave Management
- `POST /api-auth/leave_request/<emp_id>/` - Submit leave request
- `POST /api-auth/Leave-approve/<emp_id>/` - Approve or reject leave request

## API Usage Examples

### Login
```json
POST /api-auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Create Employee
```json
POST /api-auth/create-emp/
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "Phone_number": "1234567890",
  "emp_address": "123 Main St",
  "emp_gender": "M",
  "emp_department": "Backend_Developer",
  "emp_position": "senior",
  "emp_hire_date": "2024-01-15"
}
```

### Submit Leave Request
```json
POST /api-auth/leave_request/<emp_id>/
{
  "leave_type": "Casual Leave",
  "start_date": "2024-12-01",
  "end_date": "2024-12-05",
  "reason": "Personal work"
}
```

### Approve/Reject Leave
```json
POST /api-auth/Leave-approve/<emp_id>/
{
  "request_leave": 1,
  "status": "Approved",
  "reason": "Approved as per policy"
}
```

## Project Structure

```
emp/
├── api/                    # REST API application
│   ├── views.py           # API view classes
│   ├── serializers.py    # Data serializers
│   ├── urls.py           # API URL patterns
│   └── permissions.py    # Custom permissions
├── empcrud/              # Main application
│   ├── models.py        # Database models
│   ├── views.py         # Django form views
│   ├── forms.py         # Django forms
│   └── templates/       # HTML templates
├── emp/                 # Project settings
│   ├── settings.py      # Django settings
│   └── urls.py         # Main URL configuration
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Models

### User
- Custom user model with email authentication
- Role-based access (Admin/Employee)

### EmployeeDetail
- Employee information (address, gender, department, position, hire date)
- Linked to User model

### EmpAttendence
- Daily attendance records
- Check-in and check-out times
- Status tracking

### LeaveRequest
- Leave type (Sick, Casual, Annual, etc.)
- Start and end dates
- Reason and application date
- Prevents overlapping leave requests

### LeaveApproved
- Approval/rejection status
- Approved by (manager/admin)
- Reason for approval/rejection
- Prevents duplicate approvals

### Project
- Project details and status
- Project lead and members
- Deadline tracking

### Task
- Task assignment to employees
- Task status (To_Do, In_Progress, Completed)
- Linked to projects

## Features in Detail

### Leave Request Overlap Prevention
The system automatically prevents employees from submitting overlapping leave requests. When approving a leave, it also checks for conflicts with already approved leaves.

### Attendance Tracking
- Employees can check in and check out daily
- System prevents duplicate check-ins/check-outs
- Attendance reports available for each employee

### Search and Filtering
Employee list supports:
- Search by username, department, or position
- Filter by department
- Filter by position
- Filter by gender

## Permissions

- **IsAdminUser**: Admin-only access
- **IsEmployeeUser**: Employee access (can only view/edit their own data)
- **IsAuthenticated**: Requires login

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

**Faizan**
- GitHub: [@faizan1-stack](https://github.com/faizan1-stack)

## Support

For support, email your-email@example.com or open an issue in the repository.

## Acknowledgments

- Django Documentation
- Django REST Framework Documentation

