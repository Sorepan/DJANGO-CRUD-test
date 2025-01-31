from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone

from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
@login_required
def tasks(request):
    return render(request, 'tasks.html', {
        'type': 'Pending',
        'tasks': Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by("created"),
    })

@login_required
def completed_tasks(request):
    return render(request, 'tasks.html', {
        'type': 'Completed',
        'tasks': Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by("created"),
    })

@login_required
def create_task(request):
    if request.method != "POST":
        return render(request, 'create_task.html', {
            'form': TaskForm,
        })
    else:
        form = TaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()

            return redirect('tasks')

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task.html', {
        'task': task,
    })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()

        return redirect('tasks')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(instance=task, data=request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()

            return redirect('task', task_id=task_id)
    else:
        return render(request, 'edit_task.html', {
            'form': form,
            'task': task,
        })

def delete_task(request, task_id):
    if request.method == "POST":
        Task.objects.filter(id=task_id).delete()

        return redirect('tasks')


@login_required
def signout(request):
    logout(request)

    return redirect('home')

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if not user:
            return render(request, 'login.html', {
            'form': AuthenticationForm(),
            'error': "Invalid User or Password",
        })
        else:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'login.html', {
            'form': AuthenticationForm(),
        })
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        input = request.POST
        
        if not input['password1'] or not input['password2']:
            return render(request, 'sign_up.html', {
                'form': form,
                'error': "Please fill all camps",
            })
        elif input['password1'] != input['password2']:
            return render(request, 'sign_up.html', {
                'form': UserCreationForm(),
                'error': "The passwords don't match",
            })
        else:
            try:
                user = User.objects.create_user(input['username'], password=input['password1'])
                user.save()

                login(request, user)

                return redirect('tasks')
            except IntegrityError:
                return render(request, 'sign_up.html', {
                'form': UserCreationForm(),
                'error': "That username is already taken",
            })

    else:
        return render(request, 'sign_up.html', {
                'form': UserCreationForm(),
            })
