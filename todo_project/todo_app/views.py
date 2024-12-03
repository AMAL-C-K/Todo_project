from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from todo_app.models import Todo
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def signup(request):
    if request.method == 'POST':
        name = request.POST['first_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
        elif password != password2:
            messages.error(request, 'password not matching')
        elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', password):
            messages.error(request, 'password contains atleast one (0-9),(a-z),(A-Z) special characters ')
        
        else:
            user = User.objects.create_user(first_name=name, email=email, username=username, password=password)
            user.save()
            return redirect('signin')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add_todo')
        else:
            messages.error(request, 'invalid credentials')
    return render(request, 'signin.html')

def signout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/')
def add_todo(request):
    if request.method == 'POST':
        task = request.POST['task']
        tasks = Todo.objects.create(task=task, user=request.user)
        tasks.save()
    tasks = Todo.objects.filter(user=request.user,completed=False)    
    return render(request, 'todo.html', {'tasks':tasks})

@login_required(login_url='/')
def completed(request, task_id):
    task = Todo.objects.get(id=task_id,user=request.user )
    task.completed=True
    task.save()
    return redirect('add_todo')

@login_required(login_url='/')
def delete(request, task_id):
    task = Todo.objects.filter(id=task_id, user=request.user, completed=True)
    task.delete()
    return redirect('completed_list')  

@login_required(login_url='/')
def completed_list(request):
    completed = Todo.objects.filter(user=request.user, completed=True)
    return render(request, 'list.html', {'completed':completed})