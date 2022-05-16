from http.client import HTTPResponse
from django.forms import model_to_dict
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import StudentForm1,StudentForm2,StudentForm3,StudentForm,AdminForm
from formtools.wizard.views import SessionWizardView
from .models import Student,FinalStudent
from django.template import loader
FORMS=[('first',StudentForm1),('second',StudentForm2),('third',StudentForm3)]
TEMPLATES={'first':'S1.html','second':'S2.html','third':'S3.html'}
def index(request):
    form= StudentForm()
    if request.method=='POST':
        form= StudentForm(request.POST)
        if form.is_valid():
            form.save()           
    context={'form':form}
    return render(request,'basicform/index.html',context)
class StudentWizard(SessionWizardView):
    # def get_template_names(self):
    #     return [TEMPLATES[self.steps.current]]
    template_name='student_form.html'
    def done(self,form_list,**kwargs):
        form_data=process_form_data(form_list)
        fdict={}
        for i in form_data:
            for j in i:fdict[j]=i[j]
        s=Student(**fdict)
        s.save()
        jkey=s.id
        return render(None,'done.html',{'form_data':form_data,'key':jkey})
def process_form_data(form_list):
    form_data=[form.cleaned_data for form in form_list]
    return form_data
def find_student(request,hkey):
    try:
        s=Student.objects.get(pk=hkey)
        dic=model_to_dict(s)
        if request.method=='POST':
            if 'add' in request.POST:
                dic.pop('id')
                f=FinalStudent(**dic) 
                f.save()
                s=''
                if f.branch=='Computer':s=s+'C2K22'
                if f.branch=='Data Science':s=s+'D2K22'
                if f.branch=='IT':s=s+'I2K22'
                if f.branch=='ENTC':s=s+'E2K22'
                s=s+str(f.id+1000000)
                f.reg_no=s
                f.save()
                print('hello',f.id)
                dict=model_to_dict(f)  
                
                context={'dict':dict}
                return render(request,'FinalStudent.html',context)     
            if 'remove' in request.POST:
                Student.objects.filter(id=hkey).delete()
                return HttpResponse('Student Removed')
        context={'dic':dic,'hkey':hkey}
        return render(request,'showstudent.html',context)
    except Student.DoesNotExist:
        return HttpResponse("No object")
def misadmin(request):
    form=AdminForm()
    if request.method=='POST':
        form=AdminForm(request.POST)
        if form.is_valid():
           hkey=form.cleaned_data['uid']
           return HttpResponseRedirect(hkey)
    context={'form':form}
    return render(request,'admins.html',context)  