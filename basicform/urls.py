from django.urls import path, re_path
from . import views
from .views import ShowPending,DisplayFStudent
urlpatterns = [
    path('', views.index, name='index'),
    path('misadmin/',views.misadmin,name='admin'),
    path('student/',views.testrun,name='student'),
    path('viewform/',views.ViewForm,name='viewform'),
    path('showpending/',ShowPending.as_view(),name='showpending'),
    path('loginuser/',views.loginUser,name='login'),
    path('logoutuser/',views.logoutUser,name='logout'),
    path('showstudents/',DisplayFStudent.as_view(),name='studentlist'),
    path('generatereports/',views.GenerateReports,name='generaterprts'),
    path('removestudent/',views.RemoveStudent,name='rmvstudent'),
    re_path(r'misadmin/(?P<hkey>.{27})',views.find_student,name='fstudent'),
    re_path(r'showstudents/(?P<hkey>.{11})',views.find_final_student,name='fstudent'),
    re_path(r'removestudent/(?P<rollno>.{11})',views.FinalRemove,name='fremove'),
    # path('showstudent/',views.showstudent,name='showstudent')
]