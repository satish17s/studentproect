from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import StudentForm
from .models import Student
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'studentapp/home.html')

def signupuser(request):
    if request.method=='GET':
        return render(request,'studentapp/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentlist')
            except IntegrityError:
                return render(request,'studentapp/signupuser.html',{'form':UserCreationForm(),'error':'username already exist,use different username'})
        else:
            return render(request,'studentapp/signupuser.html',{'form':UserCreationForm(),'error':'password do not match'})


def loginuser(request):
    if request.method=='GET':
        return render(request,'studentapp/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'studentapp/loginuser.html',{'form':AuthenticationForm(),'error':'username and password did not match'})
        else:
            login(request,user)
            return redirect('currentlist')


def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')


@login_required
def currentlist(request):
    students=Student.objects.filter(user=request.user)
    return render(request,'studentapp/currentlist.html',{'students':students})


@login_required
def viewlist(request,student_pk):
    student=get_object_or_404(Student,pk=student_pk,user=request.user)
    if request.method=='GET':
        form=StudentForm(instance=student)
        return render(request,'studentapp/viewlist.html',{'student':student,'form':form})
    else:
        try:
            form=StudentForm(request.POST,instance=student)
            form.save()
            return redirect('currentlist')
        except ValueError:
            return render(request,'studentapp/viewlist.html',{'student':student,'form':form,'error':'bad data input'})


@login_required
def createlist(request):
    if request.method=='GET':
        return render(request,'studentapp/createlist.html',{'form':StudentForm()})
    else:
        try:
            form=StudentForm(request.POST)
            newstudent=form.save(commit=False)
            newstudent.user=request.user
            newstudent.save()
            return redirect('currentlist')
        except ValueError:
            return render(request,'studentapp/createlist.html',{'form':StudentForm,'error':'bad data input'})



@login_required
def deletestudent(request,student_pk):
    student=get_object_or_404(Student,pk=student_pk,user=request.user)
    if request.method=='POST':
        student.delete()
        return redirect('currentlist')
