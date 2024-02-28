from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib import messages


# Create your views here.
def admin_home(request):
    # emp=Employee.objects.all()
    return render(request,'admin_side/index.html')

def all_jobs():
    all_jobs=Job_type.objects.all()
    return all_jobs

def all_employee():
    all_employee=Employee.objects.all()
    return all_employee
# <-----------------login      logout------------------->

def login_user(request):
    if request.method=='POST':
        name=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=name,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['admin']=name
            return redirect(admin_home)
        else:
            messages.success(request,'Invalid username and Password')
            return redirect(login_user)    
    else:
        
        return render(request,'admin_side/login.html')    



def logout_user(request):
    if 'admin' in request.session:
        auth.logout(request)
    return redirect(login_user)




def main_fun(request):
    return redirect(login_user)





def add_user(request):
    if request.method=='POST':
        emp_id=request.POST['emp_id']
        name=request.POST['name']
        email=request.POST['email']
        ph_no=request.POST['ph_no']
        salary=request.POST['salary']
        doj=request.POST['doj']

        job_type=Job_type.objects.get(position=request.POST['position'])

        try:
            emp=Employee.objects.create(emp_id=emp_id,name=name,email=email,ph_no=ph_no,salary=salary,job_type=job_type,doj=doj)
            emp.save()
            messages.success(request,'Employee details added')
        except:
         
            messages.success(request,"Employee id already exists")
        return redirect(add_user)
    else:

        return render(request,'admin_side/add_user.html',{'job_type':all_jobs()})



def add_job_type(request):
    if request.method=='POST':
        position=request.POST['position'].upper()
        try:
            job_type=Job_type.objects.create(position=position)
            job_type.save()
            messages.success(request,'Job_type added')
        except:
            messages.success(request,'This Job exists')
        return redirect(add_job_type)
    else:
        return render(request,'admin_side/add_job_type.html',{'job_type':all_jobs()})  


def view_added_job_types(request):
    return render(request,'admin_side/added_job_type.html',{'job_type':all_job_types()})  


def view_attendence(request):
    attendance=attendance.objectss.all()

def mark_attendence(request):
    return render(request,'admin_side/mark_attendence.html',{'employee':all_employee()}) 

from django.http import JsonResponse

def update_selected_employees(request):
    if request.method == 'POST' and request.is_ajax():
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        date = request.POST.get('date')
        attendance, created = Attendance.objects.get_or_create(employee_id=employee_id, date=date)
        attendance.status = status
        attendance.save()
        return JsonResponse({'message': 'Attendance updated successfully.'})
    return JsonResponse({'message': 'Invalid request.'}, status=400)
