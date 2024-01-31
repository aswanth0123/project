from django.db import models

# Create your models here.

class Domain(models.Model):
    domain_name=models.CharField(max_length=20,unique=True)
    discription=models.TextField()

class Job_type(models.Model):
    domain=models.ForeignKey(Domain,on_delete=models.CASCADE,null=True)
    position=models.CharField(max_length=20,unique=True)
    discription=models.TextField()
class documents(models.Model):
    path = models.CharField(max_length=255)
    content = models.TextField()
    password =models.CharField(max_length=25)
    encrypt= models.BooleanField(default=False)


class access_files(models.Model):
    job_type=models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True)
    document=models.ForeignKey(documents,on_delete=models.CASCADE,null=True)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)



class Employee(models.Model):
    emp_id=models.CharField(max_length=20)
    name=models.CharField(max_length=40)
    email=models.EmailField()
    username=models.CharField(max_length=40,unique=True)
    password=models.CharField(max_length=20)
    domain=models.ForeignKey(Domain,on_delete=models.CASCADE,null=True)
    job_type=models.ForeignKey(Job_type,on_delete=models.CASCADE,null=True)


# class AccessControlMatrix(models.Model):
#     position = models.ForeignKey(position, on_delete=models.CASCADE)
#     resource = models.CharField(max_length=255)
#     can_view = models.BooleanField(default=False)
#     can_edit = models.BooleanField(default=False)
#     can_delete = models.BooleanField(default=False)
#     can_view_file = models.BooleanField(default=False)
