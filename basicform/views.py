# from asyncio.constants import ACCEPT_RETRY_DELAY
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
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
# from formtools.wizard.views import SessionWizardView
from .models import Student,FinalStudent,DeletedStudent,Branch,Clss
from .models import Division,Subject,FPost,Faculty
from django.template import loader
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'basicform/index.html')
class ShowPending(ListView):
    model=Student
def find_student(request,hkey):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
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
                st=st+str(f.id+100000)
                f.reg_no=st
                f.save()
                dict=model_to_dict(f)  
                
                context={'dict':dict}
                return render(request,'FinalStudent.html',context)     
            if 'remove' in request.POST:
                Student.objects.filter(id=hkey).delete()
                messages.success(request,"Student removed successfully")
                return redirect('index')
        context={'dic':dic,'hkey':hkey}
        return render(request,'showstudent.html',context)
    except Student.DoesNotExist:
        return HttpResponse("No object")
def misadmin(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Administrator').exists():
        form=AdminForm()
        if request.method=='POST':
            print(list(request.POST.items()))
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
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
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
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    fslist=[f.name for f in FinalStudent._meta.get_fields()]
    fslist.remove('id')
    if request.method=="POST":
        plist=dict(request.POST.items())
        field_list=[x for x in fslist if x in plist]
        field_list.remove('academic_year')
        field_list.remove('category')
        field_list.remove('branch')
        if 'academic_year+1' in plist: field_list.append('academic_year')
        if 'category+1' in plist:field_list.append('category')
        if 'branch+1' in plist:field_list.append('branch')
        # print(dict(request.POST.items()))
        # print(field_list)
        acyr=request.POST['academic_year']
        brnch=request.POST['branch']
        ctgry=request.POST['category']
        if(brnch!='Any' and ctgry!='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,branch=brnch,category=ctgry).values(*field_list)
        elif(brnch!='Any' and ctgry=='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,branch=brnch).values(*field_list)
        elif(brnch=='Any' and ctgry!='Any'):
            q=FinalStudent.objects.filter(academic_year=acyr,category=ctgry).values(*field_list)
        else:
            q=FinalStudent.objects.filter(academic_year=acyr).values(*field_list)
        print(acyr)
        print(q)
        return render(request,'reports.html',{'q':q})
    return render(request,'generatereports.html',{'fslist':fslist})
def RemoveStudent(request):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    if request.method=="POST":
        rollno=request.POST['rollno']
        print(rollno)
        return HttpResponseRedirect(rollno)
    return render(request,'removestudent.html')
def FinalRemove(request,rollno):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    try:
        f=FinalStudent.objects.get(reg_no=rollno)
        dic=model_to_dict(f)
        if request.method=='POST':
            fdict=dict(request.POST.items())
            print(fdict)
            if 'remove' in request.POST:
                dic.pop('id')
                d=DeletedStudent(**dic)
                d.reason=request.POST['reason']
                d.save()
                f.delete() 
                messages.success(request,"Student removed successfully")
                return redirect('index')     
        context={'dic':dic,'name':f.first_name+" "+f.last_name,'roll':rollno}
        return render(request,'finalremove.html',context)
    except FinalStudent.DoesNotExist:
        return HttpResponse("No object")
class DisplayFStudent(ListView):
    model=FinalStudent
def find_final_student(request,hkey):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    try:
        s=FinalStudent.objects.get(reg_no=hkey)
        dic=model_to_dict(s)
        dic.pop('id')
        context={'dic':dic,'hkey':hkey}
        return render(request,'showfinalstudent.html',context)
    except FinalStudent.DoesNotExist:
        return HttpResponse("No object")
class DisplayDeleted(ListView):
    model=DeletedStudent
def find_deleted_student(request,hkey):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    try:
        s=DeletedStudent.objects.get(reg_no=hkey)
        dic=model_to_dict(s)
        context={'dic':dic,'hkey':hkey}
        return render(request,'showfinalstudent.html',context)
    except Student.DoesNotExist:
        return HttpResponse("No object")
def UploadCsv(request):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    if request.method=='POST':
       ucsv=request.FILES['ucsv']
       data=ucsv.read().decode('utf-8')
       csv_rows=data.split('\n')
       csv1=csv_rows[0].split(',')
       if '\r' in csv1[len(csv1)-1]:
            s=csv1[len(csv1)-1]
            csv1[len(csv1)-1]=s[0:len(s)-1]
       print(csv1) 
       print(len(csv1))       
       fslist=[f.name for f in FinalStudent._meta.get_fields()]
       finalfeilds=[x for x in fslist if x in csv1]
       print(len(finalfeilds))
       for i in range(1,len(csv_rows)):
            temp=csv_rows[i].split(',')
            if len(temp)==1 and temp[0]=='':continue
            if '\r' in temp[len(temp)-1]:
                s=temp[len(temp)-1]
                temp[len(temp)-1]=s[0:len(s)-1] 
                print(len(temp))
                # print(temp)
            recdict={finalfeilds[j]:temp[j] for j in range(0,len(temp))}
            try:
                f=FinalStudent(**recdict)
                f.save()
                # print(f.id)
            except IntegrityError:
                messages.success(request,"Clash in Registration Numbers"+" "+f.reg_no)
                return redirect('index')
       messages.success(request,"Data Uploaded Successfully!!!")
       return redirect('studentlist') 
    return render(request,'upload_csv.html')
def acdadmin(request):
    return render(request,'basicform/acad_admin.html')
def addbcds(request,cat):
    cat=int(cat)
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Administrator').exists(): return redirect('login')
    if request.method=="POST":
        if cat==0:
            branchname=request.POST['new branch name']
            b=Branch(branch_name=branchname)
            b.save()
            messages.success(request,"Branch Added Successfully")
            return redirect('adcls',0)
        if cat==1:
            branch=request.POST['branch name']
            classname=request.POST['new class name']
            branch_instance=get_object_or_404(Branch,pk=branch)
            c=Clss(branch_name=branch_instance,class_name=classname)
            c.save()
            messages.success(request,"Class Added Successfully")
            return redirect('adcls',1)
        if cat==2:
            branch=request.POST['branch name']
            classname=request.POST['class name']
            division=request.POST['new division name']
            branch_instance=get_object_or_404(Branch,pk=branch)
            class_instance=get_object_or_404(Clss,class_name=classname,branch_name=branch)
            d=Division(branch_name=branch_instance,class_name=class_instance,div_name=division)
            d.save()
            messages.success(request,"Division Added Successfully")
            return redirect('adcls',2)
        if cat==3:
            branch=request.POST['branch name']
            classname=request.POST['class name']
            subject=request.POST['new subject name']
            branch_instance=get_object_or_404(Branch,pk=branch)
            class_instance=get_object_or_404(Clss,class_name=classname,branch_name=branch)
            s=Subject(branch_name=branch_instance,class_name=class_instance,sub_name=subject)
            s.save()
            messages.success(request,"Subject Added Successfully")
            return redirect('adcls',3)
    context={'cat':cat}
    branches=Branch.objects.all()
    context['branches']=branches
    if cat>1:
        classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name')
        context['classes']=classes    
    return render(request,'addclass.html',context)
def addpost(request,opt):
    opt=int(opt)
    if request.method=="POST":
        if opt==0:
            postname=request.POST['post_name']
            postype=request.POST['post_type']
            p=FPost(post_name=postname,post_type=postype)
            p.save()
            messages.success(request,"Post Added Successfully")
            return redirect('addpost',0)
        else:
            facdict=dict(request.POST.items())
            facdict.pop('csrfmiddlewaretoken')
            facdict.pop('empcode')
            post_instance=get_object_or_404(FPost,pk=facdict['post_name'])
            branch_instance=get_object_or_404(Branch,pk=facdict['branch_name'])
            facdict.pop('branch_name')
            facdict.pop('post_name')
            f=Faculty(**facdict)
            f.post_name=post_instance
            f.branch_name=branch_instance
            f.save()
            messages.success(request,"Faculty Added Successfully")
            return redirect('addpost',1)
    context={'opt':opt}
    if opt==1:
        postlist=FPost.objects.all()
        branches=Branch.objects.all()
        context['postlist']=postlist
        context['branches']=branches
    return render(request,'define_posts_faclty.html',context)
def assignSubject(request):
    if request.method=="POST":
        fac=get_object_or_404(Faculty,name=request.POST['tname'])
        sub=get_object_or_404(Subject,sub_name=request.POST['sub_name'])
        sub.faculty=fac
        div=get_object_or_404(Division,div_name=request.POST['div_name'],class_name__class_name=request.POST['class name'])
        sub.division=div
        sub.save()
        messages.success(request,request.POST['tname']+" was assigned "+request.POST['sub_name']+" in div "+request.POST['div_name']+" in class "+request.POST['class name']+" "+request.POST['branch name'])
        return redirect('asgnsub')
    branches=Branch.objects.all()
    classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name')
    teachers=Faculty.objects.filter(post_name__post_type="Teaching").values('branch_name_id','name')
    divisions=Division.objects.select_related('class_name').all().values('class_name__class_name','div_name')
    subjects=Subject.objects.select_related('class_name').all().values('class_name__class_name','sub_name')
    context={'classes':classes,'branches':branches,'teachers':teachers,'divisions':divisions,'subjects':subjects}
    return render(request,'assignsubs.html',context)