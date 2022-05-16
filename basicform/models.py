import os
from django.utils.http import urlsafe_base64_encode as b64encode
from django.db import models
from django.db import IntegrityError
# Create your models here.
class Student(models.Model):
    def pkgen():
        key= b64encode(os.urandom(20))
        try:
            c=Student.objects.get(pk=key)
            return pkgen()
        except Student.DoesNotExist :
            return key
    id = models.CharField(primary_key=True,max_length=10,default=pkgen,unique=True)
    gender_list=[('M','male'),('F','female'),('O','other')]
    cap_choice_list=[(1,1),(2,2),(3,3)]
    quota_list=[('institute','insti. lvl'),('pio','pio,J&K,J&kSSS'),('NEUT','NEUT'),('OCI','OCI'),('FN','FN'),('CIWC','CIWC')]
    state_list=[('MS','MS'),('OMS','OMS')]
    area_list=[('rural','rural'),('urban','urban')]
    board_list=[('MH','maharashtra'),('CBSE','CBSE'),('ICSE','ICSE'),('Other','Other')]
    branch_list=[('Computer','Computer'),('Data Science','Data Science'),('IT','IT'),('ENTC','ENTC')]
    #  gender_list=[('M','male'),('F','female'),('O','other')]
    first_name=models.CharField(max_length=200,default='o')
    last_name=models.CharField(max_length=200,default='o')
    age=models.IntegerField(default=1)
    father_name=models.CharField(max_length=200,default='o')
    mother_name=models.CharField(max_length=200,default='o')
    father_email=models.CharField(max_length=200,default='o')
    mother_email=models.CharField(max_length=200,default='o')

    date_of_birth=models.IntegerField(default=1)
    place_of_birth=models.CharField(max_length=30,default='o')
    mobile_number=models.CharField(max_length=10,default='o')    
    caste=models.CharField(max_length=20,default='o')
    Student_mobile=models.IntegerField(default=1)
    Tele_phone=models.IntegerField(default=1)
    Blood_group=models.CharField(max_length=3,default='o')
    permanent_address=models.CharField(max_length=200,default='urban')
    District=models.CharField(max_length=30,default='o')
    pin_code=models.IntegerField(default = 1)
    state=models.CharField(max_length=30,choices=state_list,default='MS')
    country=models.CharField(max_length=20,default='o')
    local_address=models.CharField(max_length=200,default='o')
    area=models.CharField(max_length=20,choices=area_list,default='o')
    gender=models.CharField(max_length=10,choices=gender_list,default='M')
    nationality=models.CharField(max_length=20,default='o')
    domacile=models.CharField(max_length=20,default='o')
    caste=models.CharField(max_length=20, default='o')
    Religion=models.CharField(max_length=20, default='o')
    board=models.CharField(max_length=10,choices=board_list,default='MH')
    SSC_board_marks=models.FloatField(default = 1)
    HSC_board_marks=models.FloatField(default = 1)
    college_name=models.CharField(max_length=200, default='o')
    college_address=models.CharField(max_length=200, default='o')
    passing_year=models.IntegerField(default = 1)
    Jee_percentile=models.FloatField(default = 1)
    MHTCET_percentile=models.FloatField(default = 1)
    category=models.CharField(max_length=20, default='o')
    father_occupation=models.CharField(max_length=20,default='o')
    annual_income=models.IntegerField(default=1)
    academic_year=models.CharField(max_length=20,default='2021-22')
    cap_round=models.IntegerField(choices=cap_choice_list,default=1)
    quota=models.CharField(max_length=20,choices=quota_list,default='institute')
    branch=models.CharField(max_length=20,choices=branch_list,default='Computer')

    def __str__(self):
        return self.first_name+" "+self.last_name
class FinalStudent(models.Model):
    gender_list=[('M','male'),('F','female'),('O','other')]
    cap_choice_list=[(1,1),(2,2),(3,3)]
    quota_list=[('institute','insti. lvl'),('pio','pio,J&K,J&kSSS'),('NEUT','NEUT'),('OCI','OCI'),('FN','FN'),('CIWC','CIWC')]
    state_list=[('MS','MS'),('OMS','OMS')]
    area_list=[('rural','rural'),('urban','urban')]
    board_list=[('MH','maharashtra'),('CBSE','CBSE'),('ICSE','ICSE'),('Other','Other')]
    branch_list=[('Computer','Computer'),('Data Science','Data Science'),('IT','IT'),('ENTC','ENTC')]
    # def create_regno(self):
    #     s=''
    #     if self.branch=='Computer':s=s+'C2K22'
    #     if self.branch=='Data Science':s=s+'D2K22'
    #     if self.branch=='IT':s=s+'I2K22'
    #     if self.branch=='ENTC':s=s+'E2K22'
    #     s=s+str(self.id+1000000)
    #     return s
    #  gender_list=[('M','male'),('F','female'),('O','other')]
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=200,default='o')
    last_name=models.CharField(max_length=200,default='o')
    age=models.IntegerField(default=1)
    father_name=models.CharField(max_length=200,default='o')
    mother_name=models.CharField(max_length=200,default='o')
    father_email=models.CharField(max_length=200,default='o')
    mother_email=models.CharField(max_length=200,default='o')

    date_of_birth=models.IntegerField(default=1)
    place_of_birth=models.CharField(max_length=30,default='o')
    mobile_number=models.CharField(max_length=10,default='o')    
    caste=models.CharField(max_length=20,default='o')
    Student_mobile=models.IntegerField(default=1)
    Tele_phone=models.IntegerField(default=1)
    Blood_group=models.CharField(max_length=3,default='o')
    permanent_address=models.CharField(max_length=200,default='urban')
    District=models.CharField(max_length=30,default='o')
    pin_code=models.IntegerField(default = 1)
    state=models.CharField(max_length=30,choices=state_list,default='MS')
    country=models.CharField(max_length=20,default='o')
    local_address=models.CharField(max_length=200,default='o')
    area=models.CharField(max_length=20,choices=area_list,default='o')
    gender=models.CharField(max_length=10,choices=gender_list,default='M')
    nationality=models.CharField(max_length=20,default='o')
    domacile=models.CharField(max_length=20,default='o')
    caste=models.CharField(max_length=20, default='o')
    Religion=models.CharField(max_length=20, default='o')
    board=models.CharField(max_length=10,choices=board_list,default='MH')
    SSC_board_marks=models.FloatField(default = 1)
    HSC_board_marks=models.FloatField(default = 1)
    college_name=models.CharField(max_length=200, default='o')
    college_address=models.CharField(max_length=200, default='o')
    passing_year=models.IntegerField(default = 1)
    Jee_percentile=models.FloatField(default = 1)
    MHTCET_percentile=models.FloatField(default = 1)
    category=models.CharField(max_length=20, default='o')
    father_occupation=models.CharField(max_length=20,default='o')
    annual_income=models.IntegerField(default=1)
    academic_year=models.CharField(max_length=20,default='2021-22')
    cap_round=models.IntegerField(choices=cap_choice_list,default=1)
    quota=models.CharField(max_length=20,choices=quota_list,default='institute')
    branch=models.CharField(max_length=20,choices=branch_list,default='Computer')
    reg_no=models.CharField(max_length=20,default='NULL')

    def __str__(self):
        return self.first_name+" "+self.last_name