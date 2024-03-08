from django.db import models

# Create your models here.
class Job_type(models.Model):
    position=models.CharField(max_length=20,unique=True)

class Employee(models.Model):
    emp_id=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=40)
    email=models.EmailField()
    ph_no=models.IntegerField()
    salary=models.IntegerField()
    job_type=models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True)
    doj=models.DateTimeField()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False) 

class Salary_Dtls(models.Model):
    curent_salary=models.FloatField()
    month_year=models.DateField()
    total_working_days=models.IntegerField()
    total_present=models.FloatField()
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    payable_amts=models.FloatField(null=True)
    pf_amt=models.FloatField(null=True)
    esi_amt=models.FloatField(null=True)
    tax_amt=models.FloatField(null=True)
