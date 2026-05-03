from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from .forms import TaskForm
from .models import Category, Task


def setcategories():
    Category.objects.get_or_create(name="Urgent", defaults={"description": "Urgent tasks"})
    Category.objects.get_or_create(name="Delegate", defaults={"description": "Delegated tasks"})


@login_required
def task_list(request):
    tasks = Task.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    return render(request, "tasks/task_list.html", {"tasks": tasks, "search_query": search_query})


@login_required
def task_create(request):
    setcategories()

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    categories = Category.objects.all()
    return render(request, "tasks/task_add.html", {"form": form, "categories": categories})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            obj = form.save(commit=False)
            # If no new image uploaded, keep the existing image
            if not request.FILES.get('image') and task.image:
                obj.image = task.image
            obj.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    categories = Category.objects.all()
    return render(request, "tasks/task_edit.html", {"form": form, "task": task, "categories": categories})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_delete.html", {"task": task})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()

    return render(request, "tasks/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
