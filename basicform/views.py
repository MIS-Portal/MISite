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
from django.contrib.auth.hashers import make_password
from .models import Student,FinalStudent,DeletedStudent,Branch,Clss,Attendance
from .models import Division,Subject,FPost,Faculty
from django.template import loader
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.db.models import Count
from datetime import datetime,timedelta
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
                u=User.objects.create_user(f.reg_no,f.email,'pict@123')
                print(u.username,u.password)
                sgroup=Group.objects.get(name='Student')
                sgroup.user_set.add(u)
                u.save()
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
        q=Branch.objects.values_list('branch_name',flat=True)
        ct={'branches':q}
        print(q)
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
        return render(request,'Formtest.html',ct)
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
    if  not request.user.is_authenticated or request.user.username!=hkey: return redirect('login')
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
       data=ucsv.read().decode('utf-8-sig')
       csv_rows=data.split('\n')
       csv1=csv_rows[0].split(',')
       if '\r' in csv1[len(csv1)-1]:
            s=csv1[len(csv1)-1]
            csv1[len(csv1)-1]=s[0:len(s)-1]
    #    print(csv1)       
       fslist=[f.name for f in FinalStudent._meta.get_fields()]
    #    print(len(fslist))
       finalfeilds=[x for x in fslist if x in csv1]
    #    print(len(finalfeilds))
       bulklist=[]
       userlist=[]
       for i in range(1,len(csv_rows)):
            temp=csv_rows[i].split(',')
            if len(temp)==1 and temp[0]=='':continue
            if '\r' in temp[len(temp)-1]:
                s=temp[len(temp)-1]
                temp[len(temp)-1]=s[0:len(s)-1]
            # for s in range(0,56):
            #     print(finalfeilds[s],temp[s])
            # print(temp[56])
            recdict={finalfeilds[j]:temp[j] for j in range(0,len(temp))}
            f=FinalStudent(**recdict)
            u=[f.reg_no,f.email,f.first_name,f.last_name]
            userlist.append(u)
            bulklist.append(f)
       try:
            # FinalStudent.objects.bulk_create(bulklist)
            s=make_password('pict@123')
            ul=[]
            un=[]
            sgroup=Group.objects.get(name='Student')
            for i in userlist:
                uin=User(username=i[0],email=i[1],password=s,first_name=i[2],last_name=i[3])
                ul.append(uin)
                un.append(i[0])
            User.objects.bulk_create(ul)
            p=User.objects.filter(username__in=un)
            for i in p:
                sgroup.user_set.add(i)
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
            if Branch.objects.filter(branch_name=branchname).exists():
                messages.success(request,"Branch Already Exists")
                return redirect('adcls',0)
            b=Branch(branch_name=branchname)
            b.save()
            messages.success(request,"Branch Added Successfully")
            return redirect('adcls',0)
        if cat==1:
            branch=request.POST['branch name']
            classname=request.POST['new class name']
            branch_instance=get_object_or_404(Branch,pk=branch)
            if Clss.objects.filter(branch_name=branch_instance,class_name=classname).exists():
                messages.success(request,"Class Already Exists")
                return redirect('adcls',1)
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
            if Division.objects.filter(branch_name=branch_instance,class_name=class_instance,div_name=division).exists():
                messages.success(request,"Division Already Exists")
                return redirect('adcls',2)
            d=Division(branch_name=branch_instance,class_name=class_instance,div_name=division)
            subs=Subject.objects.filter(branch_name=branch_instance,class_name=class_instance)
            subs2=subs.values('sub_name')
            subset=set()
            for i in subs2:
                print(i)
                subset.add(i['sub_name'])
            print(subset)
            d.save()
            for i in subset:
                newsub=Subject(branch_name=branch_instance,class_name=class_instance,sub_name=i,division=d)
                newsub.save()
            for i in subs:
                if i.division==None:i.delete()
            messages.success(request,"Division Added Successfully")
            return redirect('adcls',2)
        if cat==3:
            branch=request.POST['branch name']
            classname=request.POST['class name']
            subject=request.POST['new subject name']
            branch_instance=get_object_or_404(Branch,pk=branch)
            class_instance=get_object_or_404(Clss,class_name=classname,branch_name=branch)
            if Subject.objects.filter(branch_name=branch_instance,class_name=class_instance,sub_name=subject).exists():
                messages.success(request,"Subject Already Exists")
                return redirect('adcls',3)
            if Division.objects.filter(branch_name=branch_instance,class_name=class_instance).exists():
                divs=Division.objects.filter(branch_name=branch_instance,class_name=class_instance)
                for i in divs:
                    s=Subject(branch_name=branch_instance,class_name=class_instance,division=i)
                    s.sub_name=subject
                    s.save()
            else:
                s=Subject(branch_name=branch_instance,class_name=class_instance,sub_name=subject)
                s.save()
            messages.success(request,"Subject Added Successfully")
            return redirect('adcls',3)
    context={'cat':cat}
    branches=Branch.objects.all()
    branchlist=branches.values()
    divisions=Division.objects.all().values('branch_name__branch_name','class_name__class_name','div_name').order_by('branch_name__branch_name','class_name__class_name','div_name')
    subjects=Subject.objects.all().values('branch_name__branch_name','class_name__class_name','sub_name','division__div_name').order_by('branch_name__branch_name','class_name__class_name','sub_name','division__div_name')
    context['divisions']=divisions
    context['subjects']=subjects
    context['branches']=branches
    context['branchlist']=branchlist
    classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name').order_by('branch_name_id','class_name')
    context['classes']=classes  
    return render(request,'addclass.html',context)
def addpost(request,opt):
    opt=int(opt)
    if request.method=="POST":
        if opt==0:
            postname=request.POST['post_name']
            postype=request.POST['post_type']
            if FPost.objects.filter(post_name=postname,post_type=postype).exists():
                messages.success(request,"Post Already Exists")
                return redirect('addpost',0)
            p=FPost(post_name=postname,post_type=postype)
            p.save()
            messages.success(request,"Post Added Successfully")
            return redirect('addpost',0)
        else:
            facdict=dict(request.POST.items())
            facdict.pop('csrfmiddlewaretoken')
            facdict.pop('empcode')
            post_instance=get_object_or_404(FPost,pk=facdict['post_name'])
            if facdict['branch_name']!='None': branch_instance=get_object_or_404(Branch,pk=facdict['branch_name'])
            bname=facdict['branch_name']
            facdict.pop('branch_name')
            facdict.pop('post_name')
            f=Faculty(**facdict)
            f.post_name=post_instance
            if bname!='None': f.branch_name=branch_instance
            if Faculty.objects.contains(f):
                instance=get_object_or_404(Faculty,emp_code=f.emp_code)
                instance=f 
                instance.save()
                messages.success(request,"Faculty Updated Successfully")
                return redirect('addpost',1)
            f.save()
            fuser=User.objects.create_user(username=f.emp_code,password="pict@123",first_name=f.name)
            fgroup=Group.objects.get(name='Faculty')
            fuser.groups.add(fgroup)
            fuser.save()
            messages.success(request,"Faculty Added Successfully")
            return redirect('addpost',1)
    context={'opt':opt}
    if opt==1:
        postlist=FPost.objects.all()
    else: postlist=FPost.objects.all().values()
    branches=Branch.objects.all()
    faculty=Faculty.objects.values('emp_code','name','branch_name','post_name')
    context['postlist']=postlist
    context['branches']=branches
    context['faculty']=faculty
    print(postlist)
    return render(request,'define_posts_faclty.html',context)
def assignSubject(request):
    if request.method=="POST":
        fac=get_object_or_404(Faculty,name=request.POST['tname'])
        branch_instance=get_object_or_404(Branch,pk=request.POST['branch name'])
        div_instance=get_object_or_404(Division,div_name=request.POST['div_name'],branch_name=branch_instance,class_name__class_name=request.POST['class name'])
        sub=get_object_or_404(Subject,sub_name=request.POST['sub_name'],branch_name=branch_instance,division=div_instance)
        sub.faculty=fac
        div=get_object_or_404(Division,div_name=request.POST['div_name'],class_name__class_name=request.POST['class name'],branch_name=branch_instance)
        sub.division=div
        sub.save()
        messages.success(request,request.POST['tname']+" was assigned "+request.POST['sub_name']+" in div "+request.POST['div_name']+" in class "+request.POST['class name']+" "+request.POST['branch name'])
        return redirect('asgnsub')
    branches=Branch.objects.all()
    classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name').order_by('branch_name_id','class_name')
    teachers=Faculty.objects.filter(post_name__post_type="Teaching").values('branch_name_id','name','post_name__post_name').order_by('branch_name_id','name','post_name__post_name')
    divisions=Division.objects.select_related('class_name','branch_name').all().values('class_name__class_name','branch_name__branch_name','div_name').order_by('class_name__class_name','branch_name__branch_name','div_name')
    subjects=Subject.objects.select_related('class_name','branch_name','faculty','division').all().values('class_name__class_name','branch_name__branch_name','sub_name','faculty__name','division__div_name').order_by('class_name__class_name','branch_name__branch_name','division__div_name')
    
    # print(divisions,subjects)
    context={'classes':classes,'branches':branches,'teachers':teachers,'divisions':divisions,'subjects':subjects}
    return render(request,'assignsubs.html',context)
def assignclass(request):
    students=FinalStudent.objects.filter(class_name=None).values('branch','first_name','last_name','reg_no','academic_year').order_by('last_name','first_name','reg_no','academic_year')
    branches=Branch.objects.all()
    classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name').order_by('branch_name_id','class_name')
    divisions=Division.objects.select_related('class_name','branch_name').all().values('class_name__class_name','branch_name__branch_name','div_name').order_by('class_name__class_name','branch_name__branch_name','div_name')
    context={'branches':branches,'classes':classes,'students':students,'divisions':divisions}
    if request.method=='POST':
        slist=request.POST['studentlist'].split(',')
        print(dict(request.POST))
        for i in slist:
        
            brn=get_object_or_404(Branch,branch_name=request.POST['branch name'])
            std=get_object_or_404(FinalStudent,reg_no=i)
            cls=get_object_or_404(Clss,class_name=request.POST['class name'],branch_name=brn)
            div=get_object_or_404(Division,branch_name=brn,class_name=cls,div_name=request.POST['div_name'])
            std.class_name=cls
            std.division=div
            std.save()
        messages.success(request,"Assigned class and division successfully")
        return redirect('asgnclass')
    return render(request,'assign_class.html',context)
def displayClasses(request):
    students=FinalStudent.objects.values('branch','class_name__class_name','division__div_name','first_name','last_name','reg_no','academic_year').order_by('last_name','first_name','reg_no','academic_year')
    branches=Branch.objects.all()
    classes=Clss.objects.select_related('branch_name').all().values('branch_name_id','class_name').order_by('branch_name_id','class_name')
    divisions=Division.objects.select_related('class_name','branch_name').all().values('class_name__class_name','branch_name__branch_name','div_name').order_by('class_name__class_name','branch_name__branch_name','div_name')
    context={'branches':branches,'classes':classes,'students':students,'divisions':divisions}
    # print(FinalStudent.objects.filter(class_name__class_name='TE').values('first_name','last_name'))
    return render(request,'display_classlist.html',context)
def delentity(request):
    context={}
    bnchlist=[]
    declass=[]
    dediv=[]
    desub=[]
    if request.method=='POST':
        print(dict(request.POST))
        if 'delbranch' in request.POST:
            bnchlist=list(request.POST['delbranch'].strip("'").split(','))
            for i in bnchlist:
                declass=declass+list(Clss.objects.filter(branch_name=i).values_list('class_name',flat=True))
                dediv=dediv+list(Branch.objects.filter(division__branch_name=i).values_list('division__div_name',flat=True))
                desub=desub+list(Branch.objects.filter(subject__branch_name=i).values_list('subject__sub_name',flat=True))
            context['declass']=declass
            context['dediv']=dediv
            context['desub']=desub
            context['debranch']=bnchlist
            print(bnchlist)
            context['entity']=0
        if 'branches' in request.POST:
            print(dict(request.POST))
            if request.POST['confirm']=='YES':
                flist=list(request.POST['branches'].strip('[').strip(']').strip(' ').split(','))
                for i in flist:
                    print(i)
                    ins=get_object_or_404(Branch,branch_name=i.lstrip().rstrip().strip("'").strip("'"))
                    print(ins)
                    ins.delete()
                messages.success(request,"Branch/es deleted successfully")
                return redirect('adcls',0)
            else:
                return redirect('adcls',0)
        
        if 'delclass' in request.POST:
            clslist=list(request.POST['delclass'].split(','))
            for i in clslist:
                templ=list(i.split(':'))
                declass=declass+list(Clss.objects.filter(branch_name=templ[0],class_name=templ[1]).values_list('class_name',flat=True))
                dediv=dediv+list(Division.objects.filter(branch_name=templ[0],class_name__class_name=templ[1]).values_list('div_name',flat=True))
                desub=desub+list(Subject.objects.filter(branch_name=templ[0],class_name__class_name=templ[1]).values_list('sub_name',flat=True))
            context['declass']=declass
            context['dediv']=dediv
            context['desub']=desub
            context['clslist']=clslist
            context['entity']=1
        if 'classes' in request.POST:
            print(dict(request.POST))
            if request.POST['confirm']=='YES':
                flist=list(request.POST['classes'].strip("'").strip("'").strip('"').strip('"').strip('[').strip(']').split(','))
                for i in flist:
                    templ=list(i.lstrip().rstrip().strip('[').strip(']').strip("'").strip("'").strip('"').strip('"').split(':'))
                    print(templ)
                    ins=get_object_or_404(Clss,branch_name=templ[0].lstrip().rstrip(),class_name=templ[1].lstrip().rstrip()).delete()
                messages.success(request,"Class/es deleted successfully")
                return redirect('adcls',1)
            else:
                return redirect('adcls',1)
        if 'deldivision' in request.POST:
            divlist=list(request.POST['deldivision'].split(','))
            for i in divlist:
                templ=list(i.split(':'))
                dediv=dediv+list(Division.objects.filter(branch_name=templ[0],class_name__class_name=templ[1],div_name=templ[2]).values_list('div_name',flat=True))
            context['dediv']=dediv
            context['divlist']=divlist
            context['entity']=2
        if 'divisions' in request.POST:
            print(dict(request.POST))
            if request.POST['confirm']=='YES':
                flist=list(request.POST['divisions'].strip("'").strip("'").strip('"').strip('"').strip('[').strip(']').split(','))
                for i in flist:
                    templ=list(i.lstrip().rstrip().strip('[').strip(']').strip("'").strip("'").strip('"').strip('"').split(':'))
                    print(templ)
                    ins=get_object_or_404(Division,branch_name=templ[0].lstrip().rstrip(),class_name__class_name=templ[1].lstrip().rstrip(),div_name=templ[2].lstrip().rstrip()).delete()
                messages.success(request,"Division/s deleted successfully")
                return redirect('adcls',2)
            else:
                return redirect('adcls',2)
        if 'delsubject' in request.POST:
            sublist=list(request.POST['delsubject'].split(','))
            for i in sublist:
                templ=list(i.split(':'))
                desub=desub+list(Subject.objects.filter(branch_name=templ[0],class_name__class_name=templ[1],sub_name=templ[2]).values_list('sub_name',flat=True))
            context['desub']=desub
            context['sublist']=sublist
            context['entity']=3
        if 'subjects' in request.POST:
            print(dict(request.POST))
            if request.POST['confirm']=='YES':
                flist=list(request.POST['subjects'].strip("'").strip("'").strip('"').strip('"').strip('[').strip(']').split(','))
                for i in flist:
                    templ=list(i.lstrip().rstrip().strip('[').strip(']').strip("'").strip("'").strip('"').strip('"').split(':'))
                    print(templ)
                    ins=get_object_or_404(Subject,branch_name=templ[0].lstrip().rstrip(),class_name__class_name=templ[1].lstrip().rstrip(),sub_name=templ[2].lstrip().rstrip()).delete()
                messages.success(request,"Subject/s deleted successfully")
                return redirect('adcls',3)
            else:
                return redirect('adcls',3)
        if 'delfaculty' in request.POST:
            faclist=list(request.POST['delfaculty'].split(','))
            context['faclist']=faclist
            context['entity']=4
        if 'faculties' in request.POST:
            if request.POST['confirm']=='YES':
                flist=list(request.POST['faculties'].strip("'").strip("'").strip('"').strip('"').strip('[').strip(']').split(','))
                for i in flist:
                    ins=get_object_or_404(Faculty,emp_code=int(i.lstrip().rstrip().strip("'").strip("'"))).delete()
                messages.success(request,"Faculty/s deleted successfully")
                return redirect('addpost',1)
            else:
                return redirect('addpost',1)
        if  'confirm' in request.POST and request.POST['confirm']=='NO':
            return redirect('index')
    return render(request,'delent.html',context) 
def timetable(request):
    reg=request.user.username
    stu=get_object_or_404(FinalStudent,reg_no=reg)
    subs=Subject.objects.filter(branch_name=stu.branch,class_name=stu.class_name,division=stu.division,).values('sub_name','faculty__name')
    return HttpResponse('Timetable')
def attendance(request):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Faculty').exists(): return redirect('login')
    tcode=request.user.username
    userbranch=Faculty.objects.filter(emp_code=tcode).values_list('branch_name',flat=True)
    if request.method=='POST':
        if 'cls' in request.POST:
            cls=request.POST['cls']
            div=request.POST['div']
            sub=request.POST['sub']
            # print(div)
            studlist=FinalStudent.objects.filter(class_name__class_name=cls,division__div_name=div,branch=userbranch[0]).values_list('first_name','last_name','reg_no')
            ctext={'students':studlist,'teach':request.user.username,'sub':sub,'cls':cls,'div':div}
            # print(ctext)
            return render(request,'markatt.html',ctext)
        if 'students' in request.POST:
            print(dict(request.POST))
            studs=list(request.POST['students'].split(','))
            sub=request.POST['subject']
            date=request.POST['date']
            dur=request.POST['duration']
            cls=request.POST['class']
            div=request.POST['division']
            objlist=[]
            if studs!=['']:
                for i in studs:
                    print(i)
                    st=get_object_or_404(FinalStudent,reg_no=i)
                    su=get_object_or_404(Subject,sub_name=sub,class_name=st.class_name,division=st.division,branch_name__branch_name=userbranch[0])
                    # print(div,cls,userbranch[0])
                    # div=get_object_or_404(Division,div_name=div,class_name__class_name=cls,branch_name__branch_name=userbranch[0])
                    objlist.append(Attendance(subject=su,date=date,duration=dur,reg_no=st))
            if len(objlist)==0:
                su=get_object_or_404(Subject,sub_name=sub,class_name__class_name=cls,division__div_name=div,branch_name__branch_name=userbranch[0])
                a=Attendance(subject=su,date=date,duration=dur)
                a.save()
            else: Attendance.objects.bulk_create(objlist)
            messages.success(request,"Attendance Recorded Successfully")
            return redirect('index')
    classes=Subject.objects.filter(faculty__emp_code=tcode).values_list('class_name__class_name',flat=True)
    divisions=Subject.objects.filter(faculty__emp_code=tcode).distinct().values_list('division__div_name',flat=True)
    subjects=Subject.objects.filter(faculty__emp_code=tcode).values_list('sub_name',flat=True)
    context={'subjects':subjects,'classes':classes,'divisions':divisions}
    return render(request,'attendance.html',context)
def attreports(request):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Faculty').exists(): return redirect('login')
    print(request.user.groups.filter(name='Faculty').exists())
    tcode=request.user.username
    tbranch=Faculty.objects.filter(emp_code=tcode).values_list('branch_name',flat=True)
    if request.method=='POST':
        cls=request.POST['cls']
        div=request.POST['div']
        sub=request.POST['sub']
        fro=request.POST['fromdate']
        tod=request.POST['todate']
        if request.POST['type']=='Basic':
            su=get_object_or_404(Subject,sub_name=sub,class_name__class_name=cls,division__div_name=div,branch_name__branch_name=tbranch[0])
            att=Attendance.objects.filter(subject=su,date__range=[fro,tod]).values('date','duration').annotate(total=Count('reg_no',distinct=True))
            print(att)
            clstrngth=FinalStudent.objects.filter(class_name__class_name=cls,division__div_name=div,branch=tbranch[0]).count()
            for i in att:
               for j in i.keys():
                if j=='date':
                    tem=i[j]
                    i[j]=str(tem)
                elif j=='total':i[j]=clstrngth-i[j]
            blist=[]
            for i in att:
                tem=[]
                for j in i.values():
                    tem.append(j)
                blist.append(tem)
            ctext={'basiclist':blist,'cls':cls,'div':div}
            return render(request,'attrep.html',ctext)
        else:
            su=get_object_or_404(Subject,sub_name=sub,class_name__class_name=cls,division__div_name=div,branch_name__branch_name=tbranch[0])
            attr=Attendance.objects.filter(subject=su,date__range=[fro,tod]).values('date','duration').annotate(total=Count('reg_no',distinct=True)).order_by('date','duration')
            print(attr)
            clstrngth=FinalStudent.objects.filter(class_name__class_name=cls,division__div_name=div,branch=tbranch[0]).count()
            studs=FinalStudent.objects.filter(branch=tbranch[0],class_name__class_name=cls,division__div_name=div).values_list('reg_no','first_name','last_name')
            names={i[0]:i[1]+' '+i[2] for i in studs}
            # st=datetime.strptime(fro,'%Y-%m-%d')
            # et=datetime.strptime(tod,'%Y-%m-%d')
            # datelist=[]
            # while st!=et+timedelta(days=1):
            #     datelist.append(st)
            #     st+=timedelta(days=1)
            absent=Attendance.objects.filter(subject=su,date__range=[fro,tod]).values_list('date','reg_no__reg_no','duration').order_by('date','duration')
            datedict={}
            for i in attr:
                d=''
                t=0
                for key,value in i.items():
                   if key=='date':d+=str(value)+' '
                   if key=='duration':d+=str(value)+'hrs'
                   if key=='total':t=clstrngth-value
                datedict[d]=t 
            print(list(studs))
            print(absent)
            mat={}
            for i in studs:
                tem={}
                for j in datedict.keys():
                    tem[str(j)]='P'
                mat[i[0]]=tem
            for i in absent:
                if i[1]!=None: mat[i[1]][str(i[0])+' '+str(i[2])+'hrs']='A'
            for key,value in mat.items():
                print(key,value)
            att=[]
            for key,value in mat.items():
                tem=[]
                tem.append(key)
                tem.append(names[key])
                for j in value.values():
                    tem.append(j)
                att.append(tem)
            print(att)
            context={'att':att,'dates':datedict,'cls':cls,'div':div}
            return render(request,'detailatt.html',context)
    classes=Subject.objects.filter(faculty__emp_code=tcode).values_list('class_name__class_name',flat=True)
    divisions=Subject.objects.filter(faculty__emp_code=tcode).distinct().values_list('division__div_name',flat=True)
    subjects=Subject.objects.filter(faculty__emp_code=tcode).values_list('sub_name',flat=True)
    context={'subjects':subjects,'classes':classes,'divisions':divisions}
    return render(request,'get_attendance.html',context)
def studentatt(request):
    if  not request.user.is_authenticated or not request.user.groups.filter(name='Student').exists(): return redirect('login')
    studreg=request.user.username
    studself=get_object_or_404(FinalStudent,reg_no=studreg)
    if request.method=='POST':
        sub=request.POST['sub']
        fro=request.POST['fromdate']
        tod=request.POST['todate']
        su=get_object_or_404(Subject,sub_name=sub,branch_name__branch_name=studself.branch,class_name=studself.class_name,division=studself.division)
        lst=Attendance.objects.filter(subject=su,date__range=[fro,tod]).values_list('date','duration','reg_no__reg_no')
        tab={}
        for i in lst:
            d=str(i[0])+' '+str(i[1])+'hrs'
            if i[2]==studreg:tab[d]='A'
            if d not in tab.keys() or tab[d]!='A':tab[d]='P'
        context={'tab':tab}
        print(tab)
        return render(request,'studatt_report.html',context)
    subs=Subject.objects.filter(branch_name__branch_name=studself.branch,class_name=studself.class_name,division=studself.division).values_list('sub_name',flat=True)
    context={'subs':subs}
    return render(request,'get_studentatt.html',context)
def passchange(request):
    if request.method=='POST':
        oldp=request.POST['oldpass']
        newp=request.POST['newpass']
        u=authenticate(username=request.user,password=oldp)
        if u==request.user:
            u.set_password(newp)
            u.save()
            messages.success(request,("Password Changed Successfully"))
            return redirect('index')
        else:
            messages.success(request,("There was an error changing your password; Please try again :("))
            return redirect('change_password')
    return render(request,'auth/change_password.html')