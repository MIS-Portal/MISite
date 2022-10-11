from django.urls import path, re_path
from . import views
from .views import ShowPending,DisplayFStudent,DisplayDeleted
urlpatterns = [
    path('', views.index, name='index'),
    path('misadmin/',views.misadmin,name='admin'),
    path('student/',views.testrun,name='student'),
    path('viewform/',views.ViewForm,name='viewform'),
    path('showpending/',ShowPending.as_view(),name='showpending'),
    path('loginuser/',views.loginUser,name='login'),
    path('logoutuser/',views.logoutUser,name='logout'),
    path('showstudents/',DisplayFStudent.as_view(),name='studentlist'),
    path('showdelstudents/',DisplayDeleted.as_view(),name='delstudentlist'),
    path('studentrecords/',views.GenerateReports,name='studentrecords'),
    path('removestudent/',views.RemoveStudent,name='rmvstudent'),
    path('uploadcsv/',views.UploadCsv,name='ucsv'),
    path('academic_admin/',views.acdadmin,name='acdadmin'),
    path('assign_subjects/',views.assignSubject,name='asgnsub'),
    path('assign_class/',views.assignclass,name='asgnclass'),
    path('display_classlist/',views.displayClasses,name='dispclass'),
    re_path(r'addpost_faculty/(?P<opt>.{1})',views.addpost,name='addpost'),
    path('delete_entity/',views.delentity,name='delent'),
    re_path(r'addbcds/(?P<cat>.{1})',views.addbcds,name='adcls'),
    re_path(r'misadmin/(?P<hkey>.{27})',views.find_student,name='fstudent'),
    re_path(r'showstudents/(?P<hkey>.{11})',views.find_final_student,name='fstudent'),
    re_path(r'showdelstudents/(?P<hkey>.{11})',views.find_deleted_student,name='fdstudent'),
    re_path(r'removestudent/(?P<rollno>.{11})',views.FinalRemove,name='fremove'),
    # path('showstudent/',views.showstudent,name='showstudent')
]