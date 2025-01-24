from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Category

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        category = Category.objects.get(id=category_id) if category_id else None
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            completed=False
        )
        return redirect('home')
    
    sort_by = request.GET.get('sort_by', 'title')
    tasks = Task.objects.all().order_by(sort_by)
    categories = Category.objects.all()
    return render(request, 'home.html', {'tasks': tasks, 'categories': categories, 'sort_by': sort_by})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        category = Category.objects.get(id=category_id) if category_id else None
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            completed=False
        )
        return redirect('task_list')
    categories = Category.objects.all()
    return render(request, 'task_add.html', {'categories': categories})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        category_id = request.POST.get('category')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        task.completed = request.POST.get('completed') == 'on'
        task.category = Category.objects.get(id=category_id) if category_id else None
        task.save()
        return redirect('task_list')
    categories = Category.objects.all()
    return render(request, 'task_edit.html', {'task': task, 'categories': categories})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

@login_required
def vote_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.votes += 1
    task.save()
    return redirect('home')
