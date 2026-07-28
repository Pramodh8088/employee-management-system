from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # # Department
    path("departments/", views.department_list, name="department_list"),
    path("departments/add/", views.department_create, name="department_create"),
    path("departments/<int:id>/edit/", views.department_update, name="department_update"),
    path("departments/<int:id>/delete/", views.department_delete, name="department_delete"),

    # # Employee
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/<int:id>/", views.employee_detail, name="employee_detail"),
    path("employees/<int:id>/edit/", views.employee_update, name="employee_update"),
    path("employees/<int:id>/delete/", views.employee_delete, name="employee_delete"),

    # # Profile
    # path("profile/", views.profile, name="profile"),
]