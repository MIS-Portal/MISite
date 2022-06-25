from asyncio.constants import ACCEPT_RETRY_DELAY
from http.client import HTTPResponse
from multiprocessing import context
from typing import Final
from django.forms import model_to_dict
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views import View
from .forms import AdminForm
from formtools.wizard.views import SessionWizardView
from .models import Student,FinalStudent
from django.template import loader
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'basicform/index.html')
class ShowPending(ListView):
    model=Student
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
    if  not request.user.is_authenticated and not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    try:
        s=Student.objects.get(pk=hkey)
        dic=model_to_dict(s)
        if request.method=='POST':
            if 'add' in request.POST:
                dic.pop('id')
                f=FinalStudent(**dic) 
                f.save()
                s.delete()
                st=''
                if f.branch=='Computer':st=st+'C2K22'
                if f.branch=='Data Science':st=st+'D2K22'
                if f.branch=='IT':st=st+'I2K22'
                if f.branch=='ENTC':st=st+'E2K22'
                st=st+str(f.id+1000000)
                f.reg_no=st
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
    if request.user.is_authenticated and request.user.groups.filter(name='Administrator').exists():
        form=AdminForm()
        if request.method=='POST':
            form=AdminForm(request.POST)
            if form.is_valid():
               hkey=form.cleaned_data['uid']
               return HttpResponseRedirect(hkey)
            else: raise Http404("NO STUDENT")
        context={'form':form}
        return render(request,'admins.html',context)
    else: return redirect('login')  
def testrun(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fdict=dict(request.POST.items())
            print(fdict)
            fdict.pop('csrfmiddlewaretoken')
            s=Student(**fdict)
            s.save()
            jkey=s.id
            context={'fdict':fdict,'key':jkey}
            global cdict
            cdict=context
            return render(request,'done.html',context)
        return render(request,'Formtest.html')
    else: return redirect('login')
def ViewForm(request):
    if  not request.user.is_authenticated and not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    try:
        return render(request,'done.html',cdict)
    except:
        return HttpResponse("No Form Available")
def loginUser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else: 
            messages.success(request,("There was an error logging you in"))
            return redirect('/basicform/loginuser/')
    return render(request,'auth/loginUser.html')
def logoutUser(request):
    logout(request)
    messages.success(request,"YOU WERE LOGGED OUT SUCCESSFULLY!")
    return redirect('index')
def GenerateReports(request):
    if request.method=="POST":
        acyr=request.POST['academic_year']
        brnch=request.POST['branch']
        ctgry=request.POST['category']
        if(brnch!='Any' and ctgry!='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,branch=brnch,category=ctgry).values()
        elif(brnch!='Any' and ctgry=='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,branch=brnch).values()
        elif(brnch=='Any' and ctgry!='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,category=ctgry).values()
        else:
            q=FinalStudent.objects.filter(academic_year=acyr).values()
        print(acyr,brnch,ctgry)
        return render(request,'reports.html',{'q':q})
    return render(request,'generatereports.html')
class DisplayFStudent(ListView):
    model=FinalStudent

        