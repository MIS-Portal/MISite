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
    id = models.CharField(primary_key=True,max_length=28,default=pkgen,unique=True)
    gender_list=[('M','male'),('F','female'),('O','other')]
    cap_choice_list=[(0,0),(1,1),(2,2),(3,3)]
    quota_list=[('CAP','CAP'),('institute','insti. lvl'),('pio','pio,J&K,J&kSSS'),('NEUT','NEUT'),('OCI','OCI'),('FN','FN'),('CIWC','CIWC'),('TFWS','TFWS'),('EWS','EWS'),('DEF','DEF')]
    state_list=[('MS','MS'),('OMS','OMS')]
    area_list=[('rural','rural'),('urban','urban')]
    board_list=[('MH','maharashtra'),('CBSE','CBSE'),('ICSE','ICSE'),('Other','Other')]
    branch_list=[('Computer','Computer'),('Data Science','Data Science'),('IT','IT'),('ENTC','ENTC')]
    yesno_list=[('Yes','Yes'),('No','No')]
    category_list=[('SC','SC'),('ST','ST'),('OBC','OBC'),('general','general'),('VJNT','VJNT')]

    #  gender_list=[('M','male'),('F','female'),('O','other')]
    first_name=models.CharField(max_length=200,default='o')
    middle_name=models.CharField(max_length=200,default='o')
    last_name=models.CharField(max_length=200,default='o')
    age=models.IntegerField(default=1)
    father_first_name=models.CharField(max_length=200,default='o')
    mother_first_name=models.CharField(max_length=200,default='o')
    father_email=models.EmailField(max_length=200,default='xyz@gmail.com')
    mother_email=models.EmailField(max_length=200,default='xyz@gmail.com')

    father_middle_name=models.CharField(blank=True, max_length=20)
    father_last_name=models.CharField(blank=True, max_length=20)
    mother_middle_name=models.CharField(blank=True, max_length=20)
    mother_last_name=models.CharField(blank=True, max_length=20)


    date_of_birth=models.CharField(max_length=100)
    place_of_birth=models.CharField(max_length=30,default='o')
    mobile_number=models.BigIntegerField(default=1)    

    caste=models.CharField(max_length=20,default='o')
    Student_mobile=models.BigIntegerField(default=1)
    Tele_phone=models.BigIntegerField(default=1)
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
    domicile=models.CharField(max_length=20,default='o')
    caste=models.CharField(max_length=20, default='o')
    subcaste=models.CharField(max_length=20, default='o')
    Religion=models.CharField(max_length=20, default='o')
    
    HSC_board_marks=models.FloatField(default = 1)
    college_name=models.CharField(max_length=200, default='o')
    college_address=models.CharField(max_length=200, default='o')

    passing_year=models.CharField(max_length=100)

    Jee_main_percentile=models.FloatField(default = 1)
    Jee_adv_percentile=models.FloatField(default=1)
    MHTCET_percentile=models.FloatField(default = 1)
    category=models.CharField(max_length=20,choices=category_list, default='general')
    father_occupation=models.CharField(max_length=20,default='o')
    annual_income=models.IntegerField(default=1)
    academic_year=models.CharField(max_length=20,default='2021-22')
    cap_round=models.IntegerField(choices=cap_choice_list,default=1)
    quota=models.CharField(max_length=20,choices=quota_list,default='institute')
    branch=models.CharField(max_length=20,default='Computer')
    aadhar_no=models.IntegerField(default=55555)

    father_mobile=models.IntegerField( default=1)
    mother_mobile=models.IntegerField( default=1)

    email=models.EmailField(default='xyz@gmail.com')
    HSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    SSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    HSC_pcm=models.IntegerField(default=1)
    seat_type=models.CharField(max_length=100,default='o')
    first_attempt=models.CharField(max_length=3,choices=yesno_list,default='yes')
    other_info= models.CharField(blank=True,max_length=100)
    marksheet_name=models.CharField(blank=True,max_length=100)

    def __str__(self):
        return self.first_name+" "+self.last_name
class FinalStudent(models.Model):
    gender_list=[('M','male'),('F','female'),('O','other')]
    cap_choice_list=[(0,0),(1,1),(2,2),(3,3)]
    quota_list=[('CAP','CAP'),('institute','insti. lvl'),('pio','pio,J&K,J&kSSS'),('NEUT','NEUT'),('OCI','OCI'),('FN','FN'),('CIWC','CIWC'),('TFWS','TFWS'),('EWS','EWS'),('DEF','DEF')]
    state_list=[('MS','MS'),('OMS','OMS')]
    area_list=[('rural','rural'),('urban','urban')]
    board_list=[('MH','maharashtra'),('CBSE','CBSE'),('ICSE','ICSE'),('Other','Other')]
    branch_list=[('Computer','Computer'),('Data Science','Data Science'),('IT','IT'),('ENTC','ENTC')]
    yesno_list=[('Yes','Yes'),('No','No')]
    category_list=[('SC','SC'),('ST','ST'),('OBC','OBC'),('general','general'),('VJNT','VJNT')]
    reg_no=models.CharField(max_length=20,default='NULL',unique=True)
    id=models.AutoField(primary_key=True)
    #  gender_list=[('M','male'),('F','female'),('O','other')]
    first_name=models.CharField(max_length=200,default='o')
    middle_name=models.CharField(max_length=200,default='o')
    last_name=models.CharField(max_length=200,default='o')
    age=models.IntegerField(default=1)
    father_first_name=models.CharField(max_length=200,default='o')
    mother_first_name=models.CharField(max_length=200,default='o')
    father_email=models.EmailField(max_length=200,default='xyz@gmail.com')
    mother_email=models.EmailField(max_length=200,default='xyz@gmail.com')

    father_middle_name=models.CharField(blank=True, max_length=20)
    father_last_name=models.CharField(blank=True, max_length=20)
    mother_middle_name=models.CharField(blank=True, max_length=20)
    mother_last_name=models.CharField(blank=True, max_length=20)


    date_of_birth=models.CharField(max_length=100)
    place_of_birth=models.CharField(max_length=30,default='o')
    mobile_number=models.BigIntegerField(default=1)    

    caste=models.CharField(max_length=20,default='o')
    Student_mobile=models.BigIntegerField(default=1)
    Tele_phone=models.BigIntegerField(default=1)
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
    domicile=models.CharField(max_length=20,default='o')
    caste=models.CharField(max_length=20, default='o')
    subcaste=models.CharField(max_length=20, default='o')
    Religion=models.CharField(max_length=20, default='o')
    
    HSC_board_marks=models.FloatField(default = 1)
    college_name=models.CharField(max_length=200, default='o')
    college_address=models.CharField(max_length=200, default='o')

    passing_year=models.CharField(max_length=100)

    Jee_main_percentile=models.FloatField(default = 1)
    Jee_adv_percentile=models.FloatField(default=1)
    MHTCET_percentile=models.FloatField(default = 1)
    category=models.CharField(max_length=20,choices=category_list, default='general')
    father_occupation=models.CharField(max_length=20,default='o')
    annual_income=models.IntegerField(default=1)
    academic_year=models.CharField(max_length=20,default='2021-22')
    cap_round=models.IntegerField(choices=cap_choice_list,default=0)
    quota=models.CharField(max_length=20,choices=quota_list,default='institute')
    branch=models.CharField(max_length=20,default='Computer')
    aadhar_no=models.IntegerField(default=55555)

    father_mobile=models.IntegerField( default=1)
    mother_mobile=models.IntegerField( default=1)

    email=models.EmailField(default='xyz@gmail.com')
    HSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    SSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    HSC_pcm=models.IntegerField(default=1)
    seat_type=models.CharField(max_length=100,default='o')
    first_attempt=models.CharField(max_length=3,choices=yesno_list,default='yes')
    other_info= models.CharField(blank=True,max_length=100)
    marksheet_name=models.CharField(blank=True,max_length=100)
    class_name=models.ForeignKey('Clss',null=True,on_delete=models.SET_NULL,default=None)
    division=models.ForeignKey('Division',null=True,on_delete=models.SET_NULL,default=None)
    def __str__(self):
        return self.first_name+" "+self.last_name

class DeletedStudent(models.Model):
    gender_list=[('M','male'),('F','female'),('O','other')]
    cap_choice_list=[(0,0),(1,1),(2,2),(3,3)]
    quota_list=[('CAP','CAP'),('institute','insti. lvl'),('pio','pio,J&K,J&kSSS'),('NEUT','NEUT'),('OCI','OCI'),('FN','FN'),('CIWC','CIWC'),('TFWS','TFWS'),('EWS','EWS'),('DEF','DEF')]
    state_list=[('MS','MS'),('OMS','OMS')]
    area_list=[('rural','rural'),('urban','urban')]
    board_list=[('MH','maharashtra'),('CBSE','CBSE'),('ICSE','ICSE'),('Other','Other')]
    branch_list=[('Computer','Computer'),('Data Science','Data Science'),('IT','IT'),('ENTC','ENTC')]
    yesno_list=[('Yes','Yes'),('No','No')]
    category_list=[('SC','SC'),('ST','ST'),('OBC','OBC'),('general','general'),('VJNT','VJNT')]
    reg_no=models.CharField(max_length=20,default='NULL',primary_key=True)
    reason=models.CharField(max_length=200,default='NULL')
    first_name=models.CharField(max_length=200,default='o')
    middle_name=models.CharField(max_length=200,default='o')
    last_name=models.CharField(max_length=200,default='o')
    age=models.IntegerField(default=1)
    father_first_name=models.CharField(max_length=200,default='o')
    mother_first_name=models.CharField(max_length=200,default='o')
    father_email=models.EmailField(max_length=200,default='xyz@gmail.com')
    mother_email=models.EmailField(max_length=200,default='xyz@gmail.com')

    father_middle_name=models.CharField(blank=True, max_length=20)
    father_last_name=models.CharField(blank=True, max_length=20)
    mother_middle_name=models.CharField(blank=True, max_length=20)
    mother_last_name=models.CharField(blank=True, max_length=20)


    date_of_birth=models.CharField(max_length=100)
    place_of_birth=models.CharField(max_length=30,default='o')
    mobile_number=models.BigIntegerField(default=1)    

    Student_mobile=models.BigIntegerField(default=1)
    Tele_phone=models.BigIntegerField(default=1)
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
    domicile=models.CharField(max_length=20,default='o')
    caste=models.CharField(max_length=20, default='o')
    subcaste=models.CharField(max_length=20, default='o')
    Religion=models.CharField(max_length=20, default='o')
    
    HSC_board_marks=models.FloatField(default = 1)
    college_name=models.CharField(max_length=200, default='o')
    college_address=models.CharField(max_length=200, default='o')

    passing_year=models.CharField(max_length=100)

    Jee_main_percentile=models.FloatField(default = 1)
    Jee_adv_percentile=models.FloatField(default=1)
    MHTCET_percentile=models.FloatField(default = 1)
    category=models.CharField(max_length=20,choices=category_list, default='general')
    father_occupation=models.CharField(max_length=20,default='o')
    annual_income=models.IntegerField(default=1)
    academic_year=models.CharField(max_length=20,default='2021-22')
    cap_round=models.IntegerField(choices=cap_choice_list,default=0)
    quota=models.CharField(max_length=20,choices=quota_list,default='institute')
    branch=models.CharField(max_length=20,default='Computer')
    aadhar_no=models.IntegerField(default=55555)

    father_mobile=models.IntegerField( default=1)
    mother_mobile=models.IntegerField( default=1)

    email=models.EmailField(default='xyz@gmail.com')
    HSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    SSC_board=models.CharField(max_length=10,choices=board_list,default='MH')
    HSC_pcm=models.IntegerField(default=1)
    seat_type=models.CharField(max_length=100,default='o')
    first_attempt=models.CharField(max_length=3,choices=yesno_list,default='yes')
    other_info= models.CharField(blank=True,max_length=100)
    marksheet_name=models.CharField(blank=True,max_length=100)
    class_name=models.ForeignKey('Clss',null=True,on_delete=models.SET_NULL,default=None)
    division=models.ForeignKey('Division',null=True,on_delete=models.SET_NULL,default=None)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Branch(models.Model):
    branch_name=models.CharField(primary_key=True,max_length=50)
    def __str__(self):
        return self.branch_name
class Clss(models.Model):
    branch_name=models.ForeignKey('Branch',on_delete=models.CASCADE)
    class_name=models.CharField(max_length=20)
    def __str__(self):
        return self.class_name
class Division(models.Model):
    branch_name=models.ForeignKey('Branch',on_delete=models.CASCADE)
    class_name=models.ForeignKey('Clss',on_delete=models.CASCADE)
    div_name=models.CharField(max_length=20)
    def __str__(self):
        return self.div_name
class Subject(models.Model):
    branch_name=models.ForeignKey('Branch',on_delete=models.CASCADE)
    class_name=models.ForeignKey('Clss',on_delete=models.CASCADE)
    sub_name=models.CharField(max_length=50)
    faculty=models.ForeignKey('Faculty',null=True,on_delete=models.SET_NULL)
    division=models.ForeignKey('Division',null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.sub_name
class FPost(models.Model):
    choicelist=[('Teaching','Teaching'),('Non Teaching','Non Teaching')]
    post_name=models.CharField(primary_key=True,max_length=50)
    post_type=models.CharField(choices=choicelist,max_length=50)
    def __str__(self):
        return self.post_name
class Faculty(models.Model):
    emp_code=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    branch_name=models.ForeignKey('Branch',null=True,on_delete=models.SET_NULL)
    date_of_joining=models.DateField(auto_now=False, auto_now_add=False)
    post_name=models.ForeignKey("FPost", null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
class Attendance(models.Model):
    date=models.DateField()
    reg_no=models.ForeignKey('FinalStudent',on_delete=models.CASCADE,null=True)
    duration=models.IntegerField()
    subject=models.ForeignKey('Subject',on_delete=models.CASCADE)
    # division=models.ForeignKey('Division',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.duration)+str(self.reg_no)
