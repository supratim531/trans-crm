from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = ["team_id", "team_name"]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
  list_display = ["role_id", "role_name"]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
  list_display = ["emp_id", "emp_username", "emp_name", "emp_email"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ["cust_id", "cust_name", "visiting_date", "address"]
