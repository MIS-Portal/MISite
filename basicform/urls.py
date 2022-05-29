from django.urls import path, re_path
from . import views
from .forms import StudentForm1,StudentForm2,StudentForm3
from .views import StudentWizard, find_student,DisplayFStudent
urlpatterns = [
    path('', views.index, name='index'),
    path('student/', StudentWizard.as_view([StudentForm1,StudentForm2,StudentForm3])),
    path('misadmin/',views.misadmin,name='admin'),
    path('test/',views.testrun,name='test'),
    path('loginuser/',views.loginUser,name='login'),
    path('logoutuser/',views.logoutUser,name='logout'),
    path('showstudents/',DisplayFStudent.as_view(),name='studentlist'),
    re_path(r'misadmin/(?P<hkey>.{27})',views.find_student,name='fstudent'),
    # path('showstudent/',views.showstudent,name='showstudent')
]