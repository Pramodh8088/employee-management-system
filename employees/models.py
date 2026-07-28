from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    profile_image = models.ImageField(upload_to="employee_photos/", blank=True, null=True)
    address = models.TextField(blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, related_name="employees")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
