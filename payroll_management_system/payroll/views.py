from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib import messages
import datetime
import calendar
from datetime import date, timedelta
from django.utils import timezone  # If using Django models

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

def all_attendance():
    all_attendance=Attendance.objects.all()
    return all_attendance

def one_month(year,month):
    num_days = calendar.monthrange(year, month)[1]
    all_dates = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
    day=[]
    for i in range(1,len(all_dates)+1):
        day.append({'day':i,'date':all_dates[i-1]})
    sundays = sum(1 for date in all_dates if date.weekday() == calendar.SUNDAY)
    att_dtls=Attendance.objects.filter(date__gte=datetime.datetime(year, month, 1),date__lt=datetime.datetime(year, month+1, 1))
    return day,sundays,att_dtls


def add_salary():
    current_date = datetime.datetime.now()
    year = current_date.year
    month = current_date.month
    day,sundays,att_dtls=one_month(year,month-1)
    work_day=len(day)-sundays
    data=Salary_Dtls.objects.filter(month_year__gte=datetime.datetime(year, month-1, 1),month_year__lt=datetime.datetime(year, month, 1))
    if not(data):
        for i in all_employee():
            c=0
            for j in att_dtls:
                if i.id is j.employee.id:
                    c+=1
            pay_amt=(i.salary/work_day)*c
            data=Salary_Dtls.objects.create(curent_salary=i.salary,
            month_year=datetime.datetime(year, month-1, 1),
            total_working_days=work_day,
            total_present=c,
            employee=i,
            payable_amts=pay_amt
            )
            data.save()

    # if not(data):*

add_salary()
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
    today=Attendance.objects.filter(date=datetime.datetime.now().date())        
    if request.method == 'POST':
        for i in all_employee():
            if request.POST.get(i.emp_id):
                    print(i,'in')
                    data=Attendance.objects.create(employee=i,date=datetime.datetime.now().date(),status=True)
                    data.save()
            else:
                print('not',i)
    return render(request,'admin_side/mark_attendence.html',{'employee':all_employee(),'today':today}) 



def attendance_details(request):
    if request.method=='POST':
        a = request.POST['month']
        year, month = a.split('-')
        month=int(month)
        year=int(year)
    else:
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
    day,sundays,att_dtl=one_month(year,month)
    month_name = calendar.month_name[month]

    att_dtl=att_dtl

    return render(request,'admin_side/attendance_details.html',{'attendance':all_attendance(),'employee':all_employee(),'days':day,'Month':month_name,'year':year}) 


def salary_details(request):
    if request.method=='POST':
        pass
    else:
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
    day,sundays,att_dtls=one_month(year,month)
    data=Salary_Dtls.objects.filter(month_year__gte=datetime.datetime(year, month-1, 1),month_year__lt=datetime.datetime(year, month, 1))

    return render(request,'admin_side/salary_details.html',{'employee':all_employee,'data':data}) 

