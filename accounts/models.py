from django.db import models
import datetime                                   

# Create your models here.

from django.contrib.auth.models import User

# class Permission(models.Model):
#         name= models.CharField(max_length=100)   
#         def __str__(self):
#             return self.name
# class Role(models.Model):
#     name = models.CharField(max_length=100)
#     permission_classes = models.ManyToManyField(Permission)
#     def __str__(self):
#         return self.name
    
# class User_Role(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
#     def __str__(self):
        
#         return str(self.user)+" "+str(self.role)
# class User_prmissions(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     permissions = models.ForeignKey(Permission,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.user
class Speciality(models.Model):

    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)
  
    def __str__(self):
    
        return self.name

class Doctor(models.Model):
    GENDER = (('Male', 'MALE'), 
    ('Female','FEMALE'),('Others', 'OTHERS')
    )
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    doctorId  = models.CharField(max_length=100,unique=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address= models.CharField(max_length=200,null=True, blank=True)
    gender = models.CharField(choices=GENDER , max_length=20,null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    clinicAddress = models.CharField(max_length=100, null=True, blank=True)
    AppointmentPrice = models.IntegerField(null=True, blank=True)
    speciality = models.ManyToManyField(Speciality, default="General")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
    
         return self.doctorId


class DoctorSchedule(models.Model):
    DAYS = (('Monday', 'Monday'), 
    ('Tuesday','Tuesday'),('Wednseday', 'Wednseday'),('Thursday', 'Thursday')
    ,('Friday', 'Friday'),('Saturday', 'Saturday'),
    )
    doctor =  models.ForeignKey(Doctor, on_delete=models.CASCADE)
    dayAvailable = models.CharField(max_length=40,choices=DAYS)
    From = models.TimeField()
    To = models.TimeField()

    def __str__(self):

        return str(self.doctor)+" "+str(self.dayAvailable)

class Patient(models.Model):
    GENDER = (('Male', 'MALE'), 
    ('Female','FEMALE'),('Others', 'OTHERS')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patientId  = models.CharField(max_length=100,unique=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address= models.CharField(max_length=200,null=True, blank=True)
    gender = models.CharField(choices=GENDER , max_length=20,null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):

        return str(self.patientId)


class Appointment(models.Model):
    STATUS = (('Pending', 'PENDING'), 
    ('Approved','APPROVED'),('Cancelled', 'CANCELLED'),('Re-Schedule', 'RE-SCHEDULE')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS,default="PENDING")
    date_created = models.DateField(auto_now_add=True)
    make_appointment = models.BooleanField(default=False)
    
    def __str__(self):
        
        return str(self.patient)+" "+str(self.doctor)
    
# class Failed_login(models.Model):
#     user = models.CharField(max_length=50)
#     time = models.TimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.user