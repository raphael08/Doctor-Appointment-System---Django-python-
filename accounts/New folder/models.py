from django.db import models
import datetime

# Create your models here.

from django.contrib.auth.models import User


class Users():
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def add_user(self):
        return self.username

    def edit_user(self):
        pass

    def delete_user(self):
        pass

    def deactivate_user(self):
        pass

    def search_user(self):
        pass

    def assign_role(self):
        pass


class Speciality():
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)

    def add_speciality(self):
        pass

    def edit_speciality(self):
        pass

    def delete_speciality(self):
        pass

    def search_speciality(self):
        pass

   


class Doctor():
    GENDER = (('Male', 'MALE'),
              ('Female', 'FEMALE'), ('Others', 'OTHERS')
              )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    doctorId = models.CharField(max_length=100, primary_key=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    clinicAddress = models.CharField(max_length=100, null=True, blank=True)
    AppointmentPrice = models.IntegerField(null=True, blank=True)
    speciality = models.ManyToManyField(Speciality, default="General")

    def add_doctor(self):
        pass

    def edit_doctor(self):
        pass

    def delete_doctor(self):
        pass

    def search_doctor(self):
        pass
    def assign_speciality(self):
        pass
class doctor_speciality():
   
    doctor_id =  models.ForeignKey(Doctor, on_delete=models.CASCADE)
   
    speciality_id =  models.ForeignKey(Speciality, on_delete=models.CASCADE)

   

class DoctorSchedule():
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    dayAvailable = models.DateField()
    From = models.TimeField()
    To = models.TimeField()

    def add_schedule(self):
        pass

    def edit_schedule(self):
        pass

    def delete_schedule(self):
        pass

    def search_schedule(self):
        pass


class Patient():
    GENDER = (('Male', 'MALE'),
              ('Female', 'FEMALE'), ('Others', 'OTHERS')
              )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patientId = models.CharField(max_length=100, primary_key=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    def add_patient(self):
        pass

    def edit_patient(self):
        pass

    def delete_patient(self):
        pass

    def search_patient(self):
        pass


class Appointment():
    STATUS = (('Pending', 'PENDING'),
              ('Approved', 'APPROVED'), ('Cancelled', 'CANCELLED'), ('Re-Schedule', 'RE-SCHEDULE')
              )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS, default="PENDING")

    date_created = models.DateField(auto_now_add=True)

    def add_appointment(self):
        pass

    def edit_appointment(self):
        pass

    def delete_appointment(self):
        pass

    def search_appointment(self):
        pass
