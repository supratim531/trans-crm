from django.db import models

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_username = models.CharField(max_length=255)
    emp_name = models.CharField(max_length=255)
    emp_email = models.EmailField()
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.emp_username} ({self.emp_id})"

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    visiting_date = models.DateField()
    prospect_status = models.CharField(max_length=255)
    outcome = models.TextField()
    team_of_employee = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.cust_name} ({self.cust_id})"
