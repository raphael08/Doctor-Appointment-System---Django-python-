from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('resetpassword',views.resetpassword,name='resetpassword'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('manageappointment',views.manageappointment,name='manageappointment'),
    path('managespeciality',views.managespeciality,name='managespeciality'),
    path('addspeciality',views.add_speciality,name='addspeciality'), 
    path('managedoctor',views.managedoctor,name='managedoctor'),
    path('managepatient',views.managepatient,name='managepatient'),
    path('adminprofile',views.adminprofile,name='adminprofile'),
    path('reviews',views.reviews,name='reviews'),
    path('block',views.block,name='block'),
    path('adminchangepassword',views.adminchangepassword,name='adminchangepassword'),
    path('editdoctor/<str:pk>',views.editdoctor,name='editdoctor'),
    path('editpatient/<str:pk>',views.editpatient,name='editpatient'),
    path('blockuser/<str:pk>',views.blockuser,name='blockuser'),
    path('removedoctor/<str:pk>',views.removedoctor,name='removedoctor'),
    path('blockdoctor/<str:pk>',views.blockdoctor,name='blockdoctor'),
    path('removeuser/<str:pk>',views.removeuser,name='removeuser'),
    path('deleteuser/<str:pk>',views.deleteuser,name='deleteuser'),
    path('deletedoctor/<str:pk>',views.deletedoctor,name='deletedoctor'),
    path('adddoctor',views.adddoctor,name='adddoctor'),
    path('addpatient',views.addpatient,name='addpatient'),
    path('changeuserpassword/<str:pk>',views.changeuserpassword,name='changeuserpassword'),
    path('changedoctorpassword/<str:pk>',views.changedoctorpassword,name='changedoctorpassword'),
    path("manageroles",views.manageroles,name="manageroles"),
    path("addroles",views.addroles,name="addroles"),
    path("deleteroles/<str:pk>",views.deleteroles,name="deleteroles"),
    path("editroles/<str:pk>",views.editroles,name="editroles"),
    path("edit_speciality/<str:pk>",views.edit_speciality,name="edit_speciality"),
    path("delete_speciality/<str:pk>",views.delete_speciality,name="delete_speciality"),
    path("managepermissions",views.managepermissions,name="managepermissions"),
    path("grantRole/<str:pk>",views.grantRole,name="grantRole"),
    path("trash",views.trash,name="trash"),
    path("restore/<str:pk>",views.restore,name="restore"),
    path('doctorschedule',views.doctorschedule,name='doctorschedule'),
    path('adddoctorschedule',views.adddoctorschedule,name='adddoctorschele'),
    path('deletedoctorschedule/<str:pk>',views.deletedoctorschedule,name='deletedoctorschedule'),
    path('editdoctorschedule/<str:pk>',views.editdoctorschedule,name='editdoctorschedule'),
    path('makeappointment/<str:pk>',views.makeappointment,name='makeappointment'),
    path('approve_appointment/<str:pk>',views.approve_appointment,name='approve_appointment'),
    path('delete_appointment/<str:pk>',views.delete_appointment,name='delete_appointment'),
    path('cancellappointment/<str:pk>',views.cancellappointment,name='cancellappointment'),
    
    #doctor/////////////////////////////
    
    path('doctordashboard',views.doctordashboard,name='doctordashboard'),
    path('registerdoctor',views.registerdoctor,name='registerdoctor'),
    path('doctorappointment',views.doctorappointment,name='doctorappointment'),
    path('mypatient',views.mypatient,name='mypatient'),
    
    path('doctorprofile',views.doctorprofile,name='doctorprofile'),
    path('doctorchangepassword',views.doctorchangepassword,name='doctorchangepassword'),
     
    #Patient //////////////////////////////////
    
    path('patientdashboard',views.patientdashboard,name='patientdashboard'),
    path('mydoctor',views.mydoctor,name='mydoctor'),
    path('patient',views.patientprofile,name='patientprofile'),
    path('patientprofile',views.patientprofile,name='patientprofile'),
    path('patientchangepassword',views.patientchangepassword,name='patientchangepassword'),
    path('booking',views.booking,name='booking'),
    #  path('photopatient',views.photopatient,name='photopatient'),
    
     
     
]