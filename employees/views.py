from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Department, Employee
from django.db.models import Q,Sum
from django.core.paginator import Paginator
from django.contrib import messages

def home(request):
    return render(request,"employees/home.html")

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "employees/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "employees/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):

    department_count = Department.objects.count()

    employee_count = Employee.objects.count()

    latest_employees = Employee.objects.order_by("-created_at")[:5]

    total_salary = Employee.objects.aggregate(
        total=Sum("salary")
    )["total"]

    context = {
        "department_count": department_count,
        "employee_count": employee_count,
        "latest_employees": latest_employees,
        "total_salary": total_salary,
    }

    return render(
        request,
        "employees/dashboard.html",
        context,
    )   

@login_required
def department_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")

        Department.objects.create(
            name=name,
            location=location
        )  

        messages.success(request, "Department added successfully.")
        return redirect("dashboard")

    return render(request, "employees/department_form.html")

@login_required
def department_list(request):
    departments = Department.objects.all()

    context = {
        "departments": departments
    }

    return render(request, "employees/department_list.html", context)


@login_required
def department_update(request, id):
    department = get_object_or_404(Department, id=id)

    if request.method == "POST":
        department.name = request.POST.get("name")
        department.location = request.POST.get("location")

        department.save()

        messages.success(request, "Department updated successfully.")

        return redirect("department_list")

    context = {
        "department": department
    }

    return render(request, "employees/department_form.html", context)


@login_required
def department_delete(request, id):
    department = get_object_or_404(Department, id=id)

    if request.method == "POST":
        department.delete()

        messages.success(request, "Department deleted successfully.")

        return redirect("department_list")

    context = {
        "department": department
    }

    return render(request, "employees/department_confirm_delete.html", context)

@login_required
def employee_list(request):

    search_query = request.GET.get("search", "")

    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    paginator = Paginator(employees, 5)   # Show 5 employees per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
    }

    return render(
        request,
        "employees/employee_list.html",
        context
    )

@login_required
def employee_create(request):
    departments = Department.objects.all()

    if request.method == "POST":
        department = Department.objects.get(id=request.POST.get("department"))

        Employee.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            gender=request.POST.get("gender"),
            date_of_birth=request.POST.get("date_of_birth"),
            hire_date=request.POST.get("hire_date"),
            salary=request.POST.get("salary"),
            address=request.POST.get("address"),
            department=department,
            profile_image=request.FILES.get("profile_image"),
        )

        messages.success(request, "Employee added successfully.")
        return redirect("employee_list")

    context = {
        "departments": departments
    }

    return render(request,"employees/employee_form.html",
        context,
    )



@login_required
def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        employee.first_name = request.POST.get("first_name")
        employee.last_name = request.POST.get("last_name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.gender = request.POST.get("gender")
        employee.date_of_birth = request.POST.get("date_of_birth")
        employee.hire_date = request.POST.get("hire_date")
        employee.salary = request.POST.get("salary")
        employee.address = request.POST.get("address")

        employee.department = Department.objects.get(
            id=request.POST.get("department")
        )

        if request.FILES.get("profile_image"):
            employee.profile_image = request.FILES.get("profile_image")

        employee.save()

        messages.success(request, "Employee updated successfully.")
        return redirect("employee_list")

    context = {
        "employee": employee,
        "departments": departments,
    }

    return render(request, "employees/employee_form.html", context)

@login_required
def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect("employee_list")

    context =  {
                "employee": employee
            }
    return render(request,"employees/employee_confirm_delete.html",context)

@login_required
def employee_detail(request, id):

    employee = get_object_or_404(Employee, id=id)

    context = {
        "employee": employee
    }

    return render(
        request,
        "employees/employee_detail.html",
        context
    )