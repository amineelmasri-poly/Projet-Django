from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Category, Task


def setcategories():
    Category.objects.get_or_create(name="Urgent", defaults={"description": "Urgent tasks"})
    Category.objects.get_or_create(name="Delegate", defaults={"description": "Delegated tasks"})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_create(request):
    setcategories()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    categories = Category.objects.filter(name__in=["Urgent", "Delegate"])
    return render(request, "tasks/task_add.html", {"form": form, "categories": categories})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_edit.html", {"form": form, "task": task})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_delete.html", {"task": task})
