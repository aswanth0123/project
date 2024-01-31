from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
import math
import platform
import psutil


#                               Basic Datas



def all_domain():
    domain=Domain.objects.all()
    return domain
def all_job_types():
    job_type=Job_type.objects.all()
    return job_type

def all_position():
    position = Job_type.objects.all()
    return position
def ram_details():
    total=round(psutil.virtual_memory().total / (1024 ** 3), 2)
    available=round(psutil.virtual_memory().available / (1024 ** 3), 2)
    available_per=(available/total)*100
    used=round(psutil.virtual_memory().used / (1024 ** 3),2)
    used_per=(used/total)*100
    ram={
        'total': round(psutil.virtual_memory().total / (1024 ** 3), 2),  # Convert to GB
        'available': round(psutil.virtual_memory().available / (1024 ** 3), 2),  # Convert to GB
        'used': round(psutil.virtual_memory().used / (1024 ** 3), 2),  # Convert to GB
        'available_per':math.floor(available_per),
        'used_per':math.floor(used_per)
    
    }
    return ram
def rom_details():
    partitions = psutil.disk_partitions()

    # Create a list to store storage details for each partition
    storage_details = []

    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_details.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'total': math.floor(usage.total/ (1024 ** 3)),
            'used': math.floor(usage.used/ (1024 ** 3)),
            'free': math.floor(usage.free/ (1024 ** 3)),
            'free_per':100-math.floor(usage.percent),
            'percent': math.floor(usage.percent),
        })
    return storage_details


def system_info():
    system_info = platform.uname()
    cpu_info = psutil.cpu_percent(interval=1, percpu=True)

    
    d={'System':system_info.system,
        'Node_Name':system_info.node,
        'Release':system_info.release,
        'Version':system_info.version,
        'Machine':system_info.machine,
        'Processor':system_info.processor,
        # 'total': round(psutil.virtual_memory().total / (1024 ** 3), 2),  # Convert to GB
        # 'available': round(psutil.virtual_memory().available / (1024 ** 3), 2),  # Convert to GB
        # 'used': round(psutil.virtual_memory().used / (1024 ** 3), 2),  # Convert to GB
    }
    return d

import pygetwindow as gw

def get_running_browsers():

    try:
        active_window = gw.getActiveWindow()
        print('10'*10,active_window.title.replace('Access Control Matrix',''))
        return {
            'title': active_window.title,
            # 'class': active_window.class_name,
        }
    except gw.PyGetWindowException:
        return None





#                                  User datas

def add_user(request):
    if request.method=='POST':
        emp_id=request.POST['emp_id']
        name=request.POST['name']
        email=request.POST['email']
        domain=Domain.objects.get(domain_name=request.POST['d_name'])
        job_type=Job_type.objects.get(position=request.POST['position'])
        username=request.POST['uname']
        password=request.POST['password']
        try:
            emp=Employee.objects.create(emp_id=emp_id,name=name,email=email,username=username,password=password,domain=domain,job_type=job_type)
            emp.save()
            messages.success(request,'Employee details added')
        except:
            messages.success(request,'Username already exists')
        return redirect(add_user)
    else:
        domain=Domain.objects.all()
        job_type=Job_type.objects.all()
        return render(request,'admin_side/add_user.html',{'domains':domain,'job_type':job_type})

def emp_home(request):
    user=Employee.objects.get(username=request.session['emp'])
    job=Job_type.objects.get(pk=user.job_type.pk)

    files=access_files.objects.filter(job_type=job)
    e=0
    d=0
    for i in files:
        if i.document.encrypt==True:
            e+=1
        else:
            d+=1
    return render(request,'user_side/index.html',{'user':user,'system':system_info(),
            'ram':ram_details(),'rom':rom_details(),'browser':get_running_browsers(),'files':files, 'e':e,'d':d})

def view_employees(request):
    emp=Employee.objects.all()
    return render(request,'admin_side/view_employee.html',{'employee':emp})   



def user_view_files(request):
    emp=Employee.objects.get(username=request.session['emp'])
    job=Job_type.objects.get(pk=emp.job_type.pk)
    file=access_files.objects.filter(job_type=job)
    return render(request,'user_side/view_files.html',{'access_file':file})   


def user_decrypt_folder(request,id):
    if request.method=='POST':
        folder_path = request.POST.get('file')
        master_pass=request.POST['m_password']
        try:
            emp=Employee.objects.get(username=request.session['emp'],password=master_pass)
            password=request.POST['password']
            try:
                data=documents.objects.get(path=folder_path,password=password)
                key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
                enc = Encryptor(key)
                enc.decrypt_all_files(folder_path)
                data.encrypt=False
                data.save()
                messages.success(request,'Folder Decrypted')

            except:
                messages.success(request,'inavalid Folder password')
            return redirect(user_decrypt_folder,id=id)

        except:
            messages.success(request,'inavalid master password')
            return redirect(user_decrypt_folder,id=id)
    else:
        file=access_files.objects.get(pk=id)
        return render(request,'user_side/decrypt_folder.html',{'file':file})   


def user_encrypt_folder(request,id):
    if request.method=='POST':
        folder_path = request.POST.get('folder_path')
        master_pass=request.POST['m_password']
        try:
            emp=Employee.objects.get(username=request.session['emp'],password=master_pass)
            password=request.POST['password']
            try:    
                data=documents.objects.get(path=folder_path,password=password)
                key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
                enc = Encryptor(key)
                enc.encrypt_all_files(folder_path)
                data.encrypt=True
                data.save()
                messages.success(request,'Folder Decrypted')
            except:
                messages.success(request,'inavalid Folder password')
            return redirect(user_decrypt_folder,id=id)

        except:
            messages.success(request,'inavalid master password')
            return redirect(user_decrypt_folder,id=id)
    else:
        file=access_files.objects.get(pk=id)
        return render(request,'user_side/encrypt_folder.html',{'file':file})   





#                           login/logout


def main_fun(request):
    if 'emp' in request.session:
        return redirect(emp_home)
    elif 'admin' in request.session:
        return redirect(admin_home)
    else:
        return redirect(login_user)


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
            try:
                emp=Employee.objects.get(username=name,password=password)
                request.session['emp']=name
                return redirect(emp_home)
            except:
                messages.success(request,'Invalid username and Password')
                return redirect(login_user)    
    else:
        return render(request,'admin_side/login.html')    



def logout_user(request):
    if 'admin' in request.session:
        auth.logout(request)
    elif 'emp' in request.session:
        request.session.flush()
    return redirect(login_user)



#                                                      admin side





def admin_home(request):
    emp=Employee.objects.all()
    files=documents.objects.all()
    e=0
    d=0
    for i in files:
        if i.encrypt==True:
            e+=1
        else:
            d+=1
    return render(request,'admin_side/index.html',{'emp':emp,'files':files,'domain':all_domain(),'user':request.user,'position':all_position(),
            'e':e,'d':d,'system':system_info(),
            'ram':ram_details(),'rom':rom_details(),'browser':get_running_browsers()})






#                                                   Domain details

def add_domain(request):
    if request.method=='POST':
        d_name=request.POST['d_name'].upper()
        discription=request.POST['discription']
        try:
            domain=Domain.objects.create(domain_name=d_name,discription=discription)
            domain.save()
            messages.success(request,'Domain added')
        except:
            messages.success(request,'This Domain exists')
        return redirect(add_domain)
    else:
        return render(request,'admin_side/add_domain.html')  



def view_added_domains(request):
    return render(request,'admin_side/added_domains.html',{'domains':all_domain()})

def delete_domain(request,domain):
    domain=Domain.objects.get(domain_name=domain)
    domain.delete()
    messages.success(request,'domain details deleted')
    return redirect(view_added_domains)


def edit_domain(request,domain):
    domain=Domain.objects.get(domain_name=domain)
    if request.method=='POST':
        d_name=request.POST['d_name'].upper()
        discription=request.POST['discription']
        # Domain.objects.filter(domain_name=domain).update(domain_name=d_name,discription=discription)
        domain.domain_name=d_name
        domain.discription=discription
        domain.save()
        messages.success(request,'domain details Updated')
        return redirect(view_added_domains)
    else:
        return render(request,'admin_side/edit_domain.html',{'domain':domain})
    


#                                                Type Info



def add_job_type(request):
    if request.method=='POST':

        domain=Domain.objects.get(domain_name=request.POST['d_name'])
        position=request.POST['position'].upper()
        discription=request.POST['discription']
        try:
            job_type=Job_type.objects.create(domain=domain,position=position,discription=discription)
            job_type.save()
            messages.success(request,'Job_type added')
        except:
            messages.success(request,'This Job exists')
        return redirect(add_job_type)
    else:
        return render(request,'admin_side/add_job_type.html',{'domains':all_domain()})  

def view_added_job_types(request):
    return render(request,'admin_side/added_job_type.html',{'job_type':all_job_types()})  

def delete_type(request,position):
    job_type=Job_type.objects.get(position=position)
    job_type.delete()
    messages.success(request,'Job details deleted')
    return redirect(view_added_job_types)


def edit_type(request,position):
    job=Job_type.objects.get(position=position)
    if request.method=='POST':
        try:
            domain_name=request.POST['d_name']
            job.domain=Domain.objects.get(domain_name=request.POST['d_name'])
            job.position=request.POST['position'].upper()
            job.discription=request.POST['discription']
            job.save()
        except:
            job.position=request.POST['position']
            job.discription=request.POST['discription']
            job.save()
            messages.success(request,'Job_type details Updated')
            return redirect(view_added_job_types)
    else:
        return render(request,'admin_side/edit_job_type.html',{'position':job,'domains':all_domain()})





 #                                                          files and documents
    

def view_uploaded_files(request):
    files=documents.objects.all()
    return render(request,'admin_side/added_files.html',{'files':files})
 



class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self,path):
        dir_path = os.path.dirname(path)
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "/" + fname)
        return dirs

    def encrypt_all_files(self,path):
        dirs = self.getAllFiles(path)
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self,path):
        dirs = self.getAllFiles(path)
        for file_name in dirs:
            self.decrypt_file(file_name)



def upload_file(request):
    if request.method=='POST':
        folder_path = request.POST.get('folder_path')
        master_pass=request.POST['m_password']
        user=auth.authenticate(username=request.user.username,password=master_pass)
        if user is not None:
            password=request.POST['password']
            con=folder_path.strip('/')
            con=con.split('/')
            try:
                file=documents.objects.get(path=folder_path,encrypt=True)
                messages.success(request,'folder already encypted')
            except:
                document=documents.objects.create(path=folder_path,password=password,content=con[-1],encrypt=True)
                document.save()
                if os.path.exists(folder_path):
                    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
                    enc = Encryptor(key)
                    enc.encrypt_all_files(folder_path)
                    messages.success(request,'folder encypted')
                else:
                    messages.success(request,'invalid path')

        else:
            messages.success(request,'inavalid master password')
        return redirect(upload_file)
    else:
        return render(request,'admin_side/upload_file.html')


    
    
def admin_decrypt_folder(request):
    if request.method=='POST':
        folder_path = request.POST.get('folder_path')
        master_pass=request.POST['m_password']
        user=auth.authenticate(username=request.user.username,password=master_pass)
        if user is not None:
            print(user,folder_path,master_pass)
            password=request.POST['password']
            print(password)
            
            try:
                data=documents.objects.get(pk=folder_path,password=password)
                print(data)
                key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
                enc = Encryptor(key)
                enc.decrypt_all_files(data.path)
                data.encrypt=False
                data.save()
                messages.success(request,'Folder Decrypted')

            except:
                messages.success(request,'inavalid Path or password')
            return redirect(admin_decrypt_folder)

        else:
            messages.success(request,'inavalid master password')
            return redirect(admin_decrypt_folder)
    else:
        file=documents.objects.filter(encrypt=True)
        return render(request,'admin_side/decrypt_folder.html',{'file':file})

def encrypt_single_file(request):
    if request.method=='POST':
        folder_path = request.POST.get('folder_path')
        master_pass=request.POST['m_password']
        user=auth.authenticate(username=request.user.username,password=master_pass)
        if user is not None:
            password=request.POST['password']
            con=folder_path.split('/')
            print(con)
            print(con[-1])
            if os.path.exists(folder_path):
                key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
                enc = Encryptor(key)
                # enc.encrypt_all_files(folder_path)
                messages.success(request,'folder encypted')
            else:
                messages.success(request,'invalid path')

        else:
            messages.success(request,'inavalid master password')
        return redirect(upload_file)
    else:
        return render(request,'admin_side/encrypt_file.html')

def add_access(request):
    if request.method=='POST':
        document=documents.objects.get(pk=request.POST['path'])
        j_type=Job_type.objects.get(pk=request.POST['position'])
        
        try:
            read=request.POST["read"]
            read=True
        except:
            read=False
        try:
            write=request.POST["write"]
            write=True
        except:
            write=False
        access_file=access_files.objects.create(document=document,job_type=j_type,can_view=read,can_edit=write)
        access_file.save()
        messages.success(request,'access added')

        return redirect(add_access)
    else:
        document=documents.objects.all()[::-1]
        return render(request,'admin_side/add_access.html',{'document':document,'job_type':all_job_types()})



def edit_access(request):
    access_detail=access_files.objects.all()[::-1]
    return render(request,'admin_side/edit_access.html',{'access_detail':access_detail})
def editing_access(request,id):
    access_detail=access_files.objects.get(pk=id)
    if request.method=='POST':
        try:
            read=request.POST["read"]
            read=True
        except:
            read=False
        try:
            write=request.POST["write"]
            write=True
        except:
            write=False
        access_detail.can_view=read
        access_detail.save()
        return redirect(edit_access)
    else:
        return render(request,'admin_side/editing_access.html',{'access_detail':access_detail})



