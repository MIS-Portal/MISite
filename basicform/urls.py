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
    path('generatereports/',views.GenerateReports,name='"generaterprts'),
    re_path(r'misadmin/(?P<hkey>.{27})',views.find_student,name='fstudent'),
    # path('showstudent/',views.showstudent,name='showstudent')
]