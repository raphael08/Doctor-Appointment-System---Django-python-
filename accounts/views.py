from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User,auth,Permission,Group
from django.contrib import messages
from django.db.models import Q
from .models import *
from django.contrib.auth.hashers import make_password
import random 
from .forms import *
import os
import datetime
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import defaultfilters
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import formats
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
import math
from django.contrib.auth.decorators import *
from email.mime.image import MIMEImage

######### HOME ############



############ ADMIN N##################
@login_required(login_url='/login')
def dashboard(request):
    
   doctors = Doctor.objects.exclude(user__username=request.user.username).filter(is_deleted='False').filter(user__is_staff='True').order_by('id')
   patient = Patient.objects.all()[:3]
   appointment = Appointment.objects.all()
   speciality = Speciality.objects.all()
   d = doctors.count
   p = patient.count
   a = appointment.count
   s = speciality.count
   context = {'doctors':doctors,'patient': patient, 'appointment':appointment, 'd': d, 'p': p,'a':a,'s':s}
   return render(request,'admins/index.html',context) 

@login_required(login_url='/login')
def manageappointment(request):
   a= DoctorSchedule.objects.all()
   p=Patient.objects.filter(user__username=request.user.username)
   appointment = Appointment.objects.all()
   context={'a':a,'p':p,'appointment':appointment}
   return render(request,'admins/manageappointment.html',context)  

@login_required(login_url='/login')
def managespeciality(request):
    
   s = Speciality.objects.all().order_by('name')
   return render(request,'admins/managespeciality.html',{'s':s})  

@login_required(login_url='/login')
def managedoctor(request):
   u = User.objects.all()
   s = Speciality.objects.all()
   g = Group.objects.all()
   p=Permission.objects.all()
   user=User.objects.all()
   r = Permission.objects.filter(Q(user=user) | Q(group__user=user)).all()
   doctors = Doctor.objects.exclude(doctorId=1).filter(is_deleted='False').filter(user__is_staff='True').order_by('id')
   return render(request,'admins/managedoctor.html',{'doctors':doctors,'s':s,'g':g,'p':p,'r':r,'u':u})

@login_required(login_url='/login')
def managepatient(request):     
   
   g = Group.objects.all()
   patient = Patient.objects.filter(is_deleted='False').order_by('id')
   return render(request,'admins/managepatient.html',{'patient':patient,'g':g})

@login_required(login_url='/login')
def adminprofile(request):
   u = Speciality.objects.all()
   d=Doctor.objects.filter(user__id=request.user.id)
   
   try:
      p =Doctor.objects.get(user__id=request.user.id)
   except:
      pass
   if request.method =='POST':
         
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      # mname = request.POST.get("mname")
      dob = request.POST.get("dob")
      address = request.POST.get("address")
      phone = request.POST.get("phone")
      profile = request.FILES.get("profile")
      user = User.objects.filter(username=request.user.username).update(first_name=fname,last_name=lname,username=username)
      doctor=Doctor.objects.filter(id = request.user.doctor.id).update(dob=dob,address=address,phone_number=phone)
      try:
         file_name = request.FILES['profile'].name
         fs = FileSystemStorage()
         files = fs.save(profile.name,profile)
         fileurl = fs.url(files)
         report = file_name  
         doctor=Doctor.objects.filter(id = request.user.doctor.id).update(profile=profile)
      except MultiValueDictKeyError:
         file_name = False
      for i in Speciality.objects.all():
             p.speciality.remove(i.id)
      s_id = []
      spec = [x.name for x in Speciality.objects.all()]
      for x in spec:
             
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      for s in s_id:
           p.speciality.add(Speciality.objects.get(id=s)) 
      messages.success(request,'successful password changed login again')
      return redirect('/adminprofile')
   return render(request,'admins/profile.html',{'u':u,'d':d})

@login_required(login_url='/login')
def reviews(request):
   
   
   
   return render(request,'admins/reviews.html')

@login_required(login_url='/login')
def adminchangepassword(request):
   if request.method =='POST':
      old = request.POST.get("old")
      new = request.POST.get("password1")
      comf = request.POST.get("password2")
      if ((request.user.check_password(old)) and (new == comf)):
       user = User.objects.filter(username=request.user.username).update(password=make_password(new))      
 
       messages.success(request,'successful password changed login again')
       return redirect('/login')
      else:
           messages.success(request,'mismatch password')
           return redirect('/changepassword')
       
   return render(request,'admins/profile.html')

@login_required(login_url='/login')
def editdoctor(request,pk):
  
   u = Group.objects.all()
   d=Doctor.objects.filter(user__id=pk)
   p =Doctor.objects.get(user__id=pk)
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37,38,39,40]
   t = Permission.objects.exclude(id__in=exclude_perm)
   r=User.objects.get(id=pk)
  
   if request.method =='POST':

      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      # mname = request.POST.get("mname")
      dob = request.POST.get("dob")
      address = request.POST.get("address")
      phone = request.POST.get("phone")
      profile = request.FILES.get("profile")
 
      User.objects.filter(id=pk).update(first_name=fname,last_name=lname,username=username)
      Doctor.objects.filter(user_id=pk).update(dob=dob,address=address,phone_number=phone)
     
      
      for i in Group.objects.all():
             p.user.groups.remove(i.id)
             
      for j in Permission.objects.all():
              p.user.user_permissions.remove(j.id)
      
             
      s_id = []
      r_id=[]
      permission = [x.name for x in Group.objects.all()]
      perm = [i.name for i in Permission.objects.all()]
      for x in permission:
             
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      for i in perm:
             
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
           
      try:
         file_name = request.FILES['profile'].name
         fs = FileSystemStorage()
         files = fs.save(profile.name,profile)
         fileurl = fs.url(files)
         report = file_name  
         d.update(profile=profile)
      except MultiValueDictKeyError:
         file_name = False
      
      for s in s_id:
           p.user.groups.add(Group.objects.get(id=s)) 
      for r in r_id:
           p.user.user_permissions.add(Permission.objects.get(id=r))
           
      messages.success(request,'successful password changed login again')
      return HttpResponseRedirect(request.path_info)
   return render(request,'admins/editdoctor.html',{'d':d,'u':u,'t':t,'r':r})
@login_required(login_url='/login')
def editpatient(request,pk):
   
  
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37,38,39,40]
   r=User.objects.get(id=pk)
   u = Group.objects.all()
   d=Patient.objects.filter(user__id=pk)
   p =Patient.objects.get(user__id=pk)
   t = Permission.objects.all()
   if request.method =='POST': # kuvuta data za field 
         
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      mname = request.POST.get("mname")
      dob = request.POST.get("dob")
      address = request.POST.get("address")
      phone = request.POST.get("phone")
      profile = request.FILES.get("profile")
   
      
      
      u = User.objects.filter(id=pk).update(first_name=fname,last_name=lname,username=username)   
      Patient.objects.filter(user_id=pk).update(dob=dob,address=address,phone_number=phone) 
      for i in Group.objects.all():
             p.user.groups.remove(i.id)
             
      for j in Permission.objects.all():
              p.user.user_permissions.remove(j.id)
      
             
      s_id = []
      r_id=[]
      permission = [x.name for x in Group.objects.all()]
      perm = [i.name for i in Permission.objects.all()]
      for x in permission:
             
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      for i in perm:
             
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
             
      try:
         file_name = request.FILES['profile'].name
         fs = FileSystemStorage()
         files = fs.save(profile.name,profile)
         fileurl = fs.url(files)
         report = file_name  
         d.update(profile=profile)
      except MultiValueDictKeyError:
         file_name = False
      for s in s_id:
           p.user.groups.add(Group.objects.get(id=s)) 
      for r in r_id:
           p.user.user_permissions.add(Permission.objects.get(id=r))
           
      messages.success(request,'successful password changed login again')
      return HttpResponseRedirect(request.path_info) #return on same page

   return render(request,'admins/editpatient.html',{'d':d,'u':u,'p':p,'t':t})     

@login_required(login_url='/login')
def changeuserpassword(request,pk):
   u = User.objects.filter(id=pk)
   d=Patient.objects.filter(user__id=pk)
   if request.method == 'POST':
      password1= request.POST.get("password1")
      password2= request.POST.get("password2")
      if (password1==password2):
            User.objects.filter(id=pk).update(password=make_password(password1))
            return HttpResponseRedirect(request.path_info)
 
   return render(request,'admins/editpatientpassword.html',{'d':d}) 
@login_required(login_url='/login')
def changedoctorpassword(request,pk):
   u = User.objects.filter(id=pk)
   d=Doctor.objects.filter(user__id=pk)
   if request.method == 'POST':
      password1= request.POST.get("password1")
      password2= request.POST.get("password2")
      if (password1==password2):
            User.objects.filter(id=pk).update(password=make_password(password1))
            messages.info(request,"Password changed successful")
            return HttpResponseRedirect(request.path_info)
      else:
          messages.info(request,"something went wrong")  
          return HttpResponseRedirect(request.path_info) 
 
   return render(request,'admins/editdoctorpassword.html',{'d':d})      
@login_required(login_url='/login')     
def blockuser(request,pk):
       
      u = User.objects.filter(id=pk).filter(is_active='True')
     
      if u:      
       User.objects.filter(id=pk).update(is_active='False')   
      else:
         User.objects.filter(id=pk).update(is_active='True') 
      return redirect('/managepatient') 
@login_required(login_url='/login')    
def blockdoctor(request,pk):  
   p = User.objects.filter(id=pk).filter(is_active='True') and User.objects.filter(is_staff='True')
   if p:      
       User.objects.filter(id=pk).update(is_active='False')   
   else:
      User.objects.filter(id=pk).update(is_active='True') 
      return redirect('/managedoctor') 
@login_required(login_url='/login')
def adddoctor(request):
   
   u = User()
   g=Doctor()
   
   
   doctor = random.randint(1,1000)
   t = Speciality.objects.all()
   
   if request.method == 'POST':
      fname = request.POST.get("fname")
      mname = request.POST.get("mname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      phone=request.POST.get("phone")
      address=request.POST.get("address")
      if User.objects.filter(username=username).exists():
           messages.info(request,"Email already exists")
           return redirect('/managedoctor')  
      speciality = [x.name for x in Speciality.objects.all()]
      s_id = []
      role = [i.name for i in Group.objects.all()]
      r_id = []
      for x in speciality:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      for i in role:
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
      doctorId = "DR"+str(doctor)
      u.username=username
      u.first_name=fname
      u.last_name=lname
      u.is_staff='True'
      u.password=make_password("12345")
      u.save()
      
      
     
     
      g.user=u
      g.doctorId= doctorId
      
      g.phone_number=phone
      g.middle_name=mname
      g.address=address
      g.save()
      for s in s_id:
           g.speciality.add(Speciality.objects.get(id=s))
      for i in r_id:
           u.groups.add(Group.objects.get(id=i))
      
      # message = "Here is your Login credentials \n Email: "+username+"\n"+"Password: "+doctorId+"\n \n"+"Welcome Doctor"
      # send_mail('Welcome To Doctor Appointment System',message,'systemdevelopment8@gmail.com',[username],
         #  fail_silently=False)
      # msg = EmailMessage('Subject of the Email', 'Body of the email', 'systemdevelopment8@gmail.com', [username])
      # msg.content_subtype = "html"  
      # msg.attach_file('media/profile_pic/1.png')
      # msg.send()
      messages.info(request,'successful')
      return redirect('/managedoctor') 
   return render(request,'admins/managedoctor.html')
@login_required(login_url='/login')  
def addpatient(request):
   u = User()
   g=Patient()
  

   patient = random.randint(1,1000)
   if request.method == 'POST':
      fname = request.POST.get("fname")
      mname = request.POST.get("mname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      phone=request.POST.get("phone")
      address = request.POST.get("address")
      role = [x.name for x in Group.objects.all()]
      s_id = []
      if User.objects.filter(username=username).exists():
           messages.info(request,"User already exists")
           return redirect('/managepatient')  
      
      
      patientId="PT"+str(patient)
      u.username=username
      u.first_name=fname
      u.last_name=lname
     
      u.password=make_password(patientId)
      u.save()
     
      g.user=u
      g.patientId = patientId
      g.address = address
      g.phone_number=phone
      g.middle_name=mname
      for i in role:
             s_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
      
      g.save()
      for s in s_id:
           g.user.groups.add(Group.objects.get(id=s))
      
    
      # message = "Here is your Login credentials \n Email: "+username+"\n"+"Password: "+patientId+"\n \n"+"Welcome"
      # send_mail('Welcome To Doctor Appointment System',message,'systemdevelopment8@gmail.com',[username],
      #     fail_silently=False)
      
      messages.info(request,'successful')
      return redirect('/managedoctor')   
@login_required(login_url='/login')
def removedoctor(request,pk):
      u = User.objects.filter(id=pk).filter(is_active='True')
      my_date = datetime.datetime.now()
     

      if u:
           User.objects.filter(id=pk).update(is_active='False')
           Doctor.objects.filter(user__id=pk).update(is_deleted='True',deleted_at=my_date)    
           return redirect('/managedoctor')
@login_required(login_url='/login')
def removeuser(request,pk):
      u = User.objects.filter(id=pk).filter(is_active='True')
      my_date = datetime.datetime.now()
     

      if u:
           User.objects.filter(id=pk).update(is_active='False')
           Patient.objects.filter(user__id=pk).update(is_deleted='True',deleted_at=my_date)    
           return redirect('/managepatient')     
@login_required(login_url='/login')
def deleteuser(request,pk):
    
    User.objects.filter(id=pk).delete()
    
    return redirect('/trash')
@login_required(login_url='/login')
def deletedoctor(request,pk):
    
    User.objects.filter(id=pk).delete()
    
    return redirect('/trash')
       
#////////////////////////DOCTOR///////////////
@login_required(login_url='/login')
def doctordashboard(request):
   
   patient = Patient.objects.all()[:3]
   today = datetime.datetime.today()
   todayy = str(today)
   appointment = Appointment.objects.filter(doctor__doctorId=request.user.doctor.doctorId)
   a = appointment.count
   t = Patient.objects.filter(user__date_joined=todayy).count
   
   p = patient.count
   context = {'t':t,'p':p,'a':a,'appointment':appointment}
   return render(request,'doctor/dashboard.html',context)


def registerdoctor(request):
   u = User()
   g=Doctor()
   k = Group.objects.get(name="Doctor")

   doctor = random.randint(1,1000)

   t = Speciality.objects.all()
   if request.method == 'POST':
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
       
        phone=request.POST.get("phone")
        
        if User.objects.filter(username=username).exists():
           messages.info(request,"User already exists")
           return redirect('/registerdoctor')   
        speciality = [x.name for x in Speciality.objects.all()]
        s_id = []
        for x in speciality:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        if (password1 == password2):
         u.username=username
         u.first_name=fname
         u.last_name=lname
         u.is_staff='True'
         u.password=make_password(password1)
         u.save()
         u.groups.add(k)
         g.user=u
         g.doctorId="DR"+str(doctor)
         g.phone_number=phone
         g.middle_name=mname
      
         g.save()
         for s in s_id:
           g.speciality.add(Speciality.objects.get(id=s))
         messages.info(request,'successful')
         return render(request,'login.html')
        

        else:
         messages.error(request,'mismatch password')
   return render(request,'register_doctor.html',{'t':t})
@login_required(login_url='/login')
def doctorappointment(request):
       
       return render(request,'doctor/appointments.html')
@login_required(login_url='/login')
def mypatient(request):
   
   
   return render(request,'doctor/my-patients.html')
@login_required(login_url='/login')
def doctorschedule(request):
   doctors = DoctorSchedule.objects.all()
   
   c = Doctor.objects.exclude(doctorId=1).filter(is_deleted='False').filter(user__is_staff='True').order_by('id')
   return render(request,'admins/managedoctorschedule.html',{'doctors':doctors,'c':c})

def adddoctorschedule(request):
       
      if  request.method == 'POST':
       name = request.POST.get('doctor')
       dname = Doctor.objects.get(id=name)
       day = request.POST.get('day')
       fro = request.POST.get('from')
       to = request.POST.get('to')
       if (str(fro) > str(to)):
              messages.error(request,'time must be greater than from time')
              return redirect('/doctorschedule')
       DoctorSchedule.objects.create(doctor=dname,dayAvailable=day,From=fro,To=to)
       return redirect('/doctorschedule')
def deletedoctorschedule(request,pk):
       
       DoctorSchedule.objects.filter(id=pk).delete()
       return redirect('/doctorschedule')
def editdoctorschedule(request,pk):
      i=DoctorSchedule.objects.filter(id=pk)
      if  request.method == 'POST':
         
         day = request.POST.get('day')
         fro = request.POST.get('from')
         to = request.POST.get('to')
         if (str(fro) > str(to)):
              messages.error(request,'time must be greater than from time')
              return redirect('/doctorschedule')
         DoctorSchedule.objects.filter(id=pk).update(dayAvailable=day,From=fro,To=to)
         return redirect('/doctorschedule')
      return render(request,'admins/editdoctorschedule.html',{'i':i}) 
@login_required(login_url='/login')
def doctorprofile(request):
   
   
   return render(request,'doctor/doctor-profile.html')
@login_required(login_url='/login')
def doctorchangepassword(request):
   
   
   return render(request,'doctor/doctorchangepassword.html')


############## PATIENT ###################
@login_required(login_url='/login')
def patientdashboard(request):
       
   
   return render(request,'patient/patient-dashboard.html')

@login_required(login_url='/login')
def booking(request):
       
       return render(request,'patient/book.html')
@login_required(login_url='/login')
def mydoctor(request):
   
   
   return render(request,'patient/searchdoctor.html')
@login_required(login_url='/login')

@login_required(login_url='/login')
def patientprofile(request):
  
   if request.method =='POST':
         
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      mname = request.POST.get("mname")
      dob = request.POST.get("dob")
      address = request.POST.get("address")
      phone = request.POST.get("phone")
      try:
         profile = request.FILES.get("profile")
         file_name = request.FILES['profile'].name
         fs = FileSystemStorage()
         files = fs.save(profile.name,profile)
         fileurl = fs.url(files)
         report = file_name 
         user = User.objects.filter(username=request.user.username).update(first_name=fname,last_name=lname,username=username)      
         patient=Patient.objects.filter(patientId = request.user.patient.patientId).update(middle_name=mname,dob=dob,address=address,phone_number=phone,profile=profile)
         messages.success(request,'successful password changed login again')
         return redirect('/patientprofile')
      except MultiValueDictKeyError:
         file_name = False
   return render(request,'patient/patient-profile.html')
@login_required(login_url='/login')
def patientchangepassword(request):
  
  
       
   if request.method =='POST':
      old = request.POST.get("old")
      new = request.POST.get("new")
      comf = request.POST.get("comfirm")
      if ((request.user.check_password(old)) and (new == comf)):
             
      
     

       user = User.objects.filter(username=request.user.username).update(password=make_password(new))      
 
       messages.success(request,'successful password changed login again')
       return redirect('/login')
   
      
   
   
   return render(request,'patient/patientchangepassword.html')
##########################HOME############################
def home(request):
    doctors = Doctor.objects.exclude(user__username=request.user.username).filter(is_deleted='False').filter(user__is_staff='True').order_by('id')
    s = Speciality.objects.all()
    return render(request,'index.html',{'doctors':doctors,'s':s})

def register(request):
   u = User()
   g=Patient()
   k = Group.objects.get(name="Patient")

   patient = random.randint(1,1000)


   if request.method == 'POST':
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
       
        phone=request.POST.get("phone")
        if User.objects.filter(username=username).exists():
         messages.info(request,"User already exists")
         return redirect('/register')  
         

        if (password1 == password2):
         u.username=username
         u.first_name=fname
         u.last_name=lname
         
         u.password=make_password(password1)
         u.save()
         u.groups.add(k)
         g.user=u
         g.patientId="PT"+str(patient)
         g.phone_number=phone
         g.middle_name=mname
         
         g.save()

         messages.info(request,'successful')
         return render(request,'login.html')
        

        else:
         messages.error(request,'mismatch password')

    
   return render(request,'register.html')  

def block(request):

    return render(request,'lock-screen.html')

def login(request):
       #  u = User.objects.filter(is_staff='true')
    
      
    if request.method=='POST':
  
     username = request.POST.get("username")
     password = request.POST.get("password")

     user = auth.authenticate(username=username,password=password)
 
     if user is not None:
            
         if user.is_superuser: 
            auth.login(request,user)
            return redirect('/dashboard')
         elif user.is_staff:  
             auth.login(request,user)
             return redirect('/dashboard')
         else:
            auth.login(request,user)
            return redirect('/dashboard')
 
     else:
         messages.info(request,'Unknown information')
         return redirect('/login')

        
         # f = Failed_login.objects.filter(user=username).count() 
         # Failed_login.objects.create(user=username)    
         # if f == 2 :
                       
         #       User.objects.filter(username=username).update(is_active='False')
         #       return render(request,'lock-screen.html',{'u':u})         

         # return redirect('/login')
     
                   
    return render(request,'login.html')

def resetpassword(request):
      # if request.method =='POST':
      #      num = random.randint(1,1000)
      #  username = request.POST.get('username')
            
      return render(request,'forgotpassword.html')   

def logout(request):
    auth.logout(request)

    return redirect('/login')


# def send_otp(request):
#    if request.method =='POST':
#       OTP = random.randint(1000,9999)
#       s=(OTP)
#       email=request.POST.get('username')
      
#       print("the no is: "+str(s))
     
#       send_mail('OTP request',s,'systemdevelopment8@gmail.com',[email],fail_silently=True)
                         
#       return HttpResponse('sent')
#    return redirect('/verfy_code')

# def verfy_code():
#    # o=generateOTP()
   
   
#    # otp_code = request.GET.get("code")
#    # if (otp_code == o):
#    #       return HttpResponse("successful")
   
   
#    return s

# def addpermission(request):
#  p = Permission()
#  if request.method == "POST":
#       name = request.POST.get("name")
#       p.name=name
#       return redirect('/addpermission')  
#  return render(request,'addpermission.html')
@login_required(login_url='/login')
def manageroles(request):
       
      g = Group.objects.all().order_by('id')
      exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24]
      r = Permission.objects.exclude(id__in=exclude_perm)
      return render(request,'admins/manageroles.html',{'r':r,'g':g})
@login_required(login_url='/login')
def addroles(request):
   p = Group()
  
   if request.method == "POST":
      name = request.POST.get("name")
      permission = [x.name for x in Permission.objects.all()]
      s_id = []
      p.name=name
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      p.save()
      for s in s_id:
           p.permissions.add(Permission.objects.get(id=s))   
      return redirect('/manageroles')  
   return redirect('/manageroles')

# def deleteroles(request,pk):
       
#        Role.objects.filter(id=pk).delete()
       
#        return redirect('/manageroles')

@login_required(login_url='/login')

def editroles(request,pk):
   
   exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
   p = Permission.objects.exclude(id__in=exclude_perm)
   r = Group.objects.filter(id=pk)
   y=Group.objects.get(id=pk)
   if request.method == 'POST':
    name = request.POST.get('name')
    
             
    for j in Permission.objects.all():
              y.permissions.remove(j.id) 
      
      
    permission = [x.name for x in Permission.objects.all()]
     
    s_id = []
    Group.objects.filter(id=pk)
    for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
    r=Group.objects.filter(id=pk).update(name=name)
      
    for s in s_id:
           y.permissions.add(Permission.objects.get(id=s))  
    return redirect('/manageroles')
           
   return render(request,'admins/editroles.html',{'r':r,'p':p})
          
@login_required(login_url='/login')    
def managepermissions(request):
   
   u = User.objects.exclude(username=request.user.username).exclude(id=1)   
   g  = Group.objects.all()
   p=Group.objects.all()
   return render(request,'admins/managepermissions.html',{'u':u,'g':g,'p':p})

@login_required(login_url='/login')
def grantRole(request,pk):
    i = Group.objects.all()
    d=Doctor.objects.filter(user__id=pk)
    u = User.objects.get(id=pk)
    p = Permission.objects.all()
    r = Group.objects.filter(id=pk)
    f=User.objects.filter(id=pk)
    if request.method == 'POST':
      for i in Group.objects.all():
             u.groups.remove(i.id)
             
      for j in Permission.objects.all():
              u.user_permissions.remove(j.id)
      permission = [x.name for x in Group.objects.all()]
      s_id = []
     
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      
      for s in s_id:
           u.groups.add(Group.objects.get(id=s)) 
      if u.is_staff==True:
       return redirect('/managedoctor')
      else:
         return redirect('/managepatient')    
    return render(request,'admins/grantrole.html',{'d':d,'i':i,'u':u,})
@login_required(login_url='/login')   
def deleteroles(request,pk):
    
    Group.objects.filter(id=pk).delete()
    
    return redirect('/manageroles')
@login_required(login_url='/login')
def trash(request):
    
    s=Doctor.objects.filter(is_deleted='True')                  
    
    p=Patient.objects.filter(is_deleted='True')
    return render(request, 'admins/trash.html',{'s':s,'p':p})           
@login_required(login_url='/login')               
def restore(request,pk):   

  u=User.objects.filter(id=pk).filter(is_active='True')
  d=Doctor.objects.filter(user__id=pk)
  if d:
   User.objects.filter(id=pk).update(is_active='True')    
   Doctor.objects.filter(user__id=pk).update(is_deleted='False')  
   return redirect('/trash')
  else: 
   User.objects.filter(id=pk).update(is_active='True')    
   Patient.objects.filter(user__id=pk).update(is_deleted='False') 
   return redirect('/trash')             
      
@login_required(login_url='/login')    
def add_speciality(request):
   
   
   if request.method == 'POST':
      name = request.POST.get('name')
      description = request.POST.get('desc')
      image= request.FILES.get("file")
      Speciality.objects.create(name=name, description=description, image=image)
      return redirect('/managespeciality')
@login_required(login_url='/login')
def edit_speciality(request,pk):
   i=Speciality.objects.filter(id=pk)
   
   if request.method =='POST':
      name = request.POST.get('name')
      desc = request.POST.get('desc')
      profile = request.FILES.get('pic')
      i.update(name=name, description=desc)
      try: 
         file_name = request.FILES['pic'].name
         fs = FileSystemStorage()
         files = fs.save(profile.name,profile)
         fileurl = fs.url(files)
         report = file_name  
         i.update(image=profile)
      except MultiValueDictKeyError:
         file_name = False
      return redirect('/managespeciality')  
   return render(request,'admins/editspeciality.html',{'i':i})
@login_required(login_url='/login')
def delete_speciality(request,pk):
       
   Speciality.objects.get(id=pk).delete()    
   return redirect('/managespeciality') 


def makeappointment(request,pk):
   
   d=DoctorSchedule.objects.get(id=pk)
   
   
   s = request.user.patient.id
   p=Patient.objects.get(id=s)
   
      
   Appointment.objects.create(doctor=d,patient=p)
   
   return redirect('/doctorschedule')
def cancellappointment(request,pk):
       Appointment.objects.filter(id=pk).update(status='CANCELLED')
       return redirect('/manageappointment')
def approve_appointment(request,pk):
 Appointment.objects.filter(id=pk).update(status='APPROVED')

 
 return redirect('/manageappointment')

def delete_appointment(request,pk):
       
   Appointment.objects.filter(id=pk).delete()
   
   return redirect('/manageappointment')
       
      