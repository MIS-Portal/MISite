from django.forms import ModelForm
from .models import Student
from django import forms
class StudentForm(ModelForm):
    # your_name=forms.CharFeild(label='your name',max_length=100)
    class Meta:
        model = Student
        fields='__all__'
class StudentForm1(ModelForm):
    class Meta:
        model=Student
        fields={'branch','first_name','age', 'last_name','father_name','father_email','mother_name','mother_email','father_occupation','annual_income'}
class StudentForm2(ModelForm):
    class Meta:
        model=Student
        fields={'permanent_address','District','pin_code','state','country','local_address','mobile_number','Tele_phone','date_of_birth','gender','nationality','area','place_of_birth','domacile','caste','Religion'}
class StudentForm3(ModelForm):
    class Meta:
        model=Student
        fields={'SSC_board_marks','HSC_board_marks','Jee_percentile','MHTCET_percentile','college_address','passing_year','category','academic_year','cap_round','quota','board'}
class AdminForm(forms.Form):
    uid=forms.CharField()