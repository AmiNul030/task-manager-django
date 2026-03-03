from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def task_list(request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")     # all | pending | done
    priority = request.GET.get("priority", "all") # all | L | M | H

    tasks = Task.objects.all()

    if q:
        tasks = tasks.filter(title__icontains=q) | tasks.filter(description__icontains=q)

    if status == "pending":
        tasks = tasks.filter(completed=False)
    elif status == "done":
        tasks = tasks.filter(completed=True)

    if priority in ["L", "M", "H"]:
        tasks = tasks.filter(priority=priority)

    tasks = tasks.order_by("completed", "due_date", "-id")

    total = Task.objects.count()
    done = Task.objects.filter(completed=True).count()
    pending = total - done

    context = {
        "tasks": tasks,
        "q": q,
        "status": status,
        "priority": priority,
        "total": total,
        "pending": pending,
        "done": done,
    }
    return render(request, "tasks/task_list.html", context)

def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Task added!")
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form, "title": "Add New Task"})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Task updated!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form, "title": "Edit Task"})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        messages.success(request, "🗑️ Task deleted!")
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
    return redirect("task_list")