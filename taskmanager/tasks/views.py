from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # function er jonno...class hole mixin use kortam
from . models import Task, User, Profile
from . forms import TaskForm, ProfileUpdateForm, UserUpdateForm
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
@login_required
def ViewTaskList(request):
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')
    due_date_filter = request.GET.get('due_date', 'all')
    sort_by = request.GET.get('sort', 'newest')
    search_filter = request.GET.get('search')
    
    tasks = Task.objects.filter(owner = request.user)
    # tasks = Task.objects.all()
    
    if search_filter:
        tasks = tasks.filter(title__icontains = search_filter) | tasks.filter(description__icontains = search_filter)
    
    if status_filter != 'all':
        tasks = tasks.filter(status = status_filter)
    
    if priority_filter != 'all':
        tasks = tasks.filter(priority = priority_filter)
    
    if due_date_filter != 'all':
        today = timezone.now().date()
        
        if due_date_filter == 'today':
            tasks = tasks.filter(due_date = today)
        elif due_date_filter == 'this_week':
            week_start = today
            week_end = today + timedelta(days=7)
            tasks = tasks.filter(due_date__range = [week_start, week_end])
        elif due_date_filter == 'overdue':
            tasks = tasks.filter(due_date__lt = today, status__in =['pending', 'in_progress'])
        
        
    if sort_by == 'oldest':
        tasks = tasks.order_by('created_at')
    else:
        tasks = tasks.order_by('-created_at')
        
    completed_tasks = tasks.filter(status = 'complete')
    pending_tasks = tasks.filter(status__in = ['pending', 'in_progress'])   
        
    context = {
        'tasks' : tasks,
        'search_filter' : search_filter,
        'status_filter': status_filter,
        'priority_filter' : priority_filter,
        'due_date_filter' : due_date_filter,
        'sort_by' : sort_by,
        'completed_tasks' : completed_tasks,
        'pending_tasks' : pending_tasks,
    }
    return render(request, "tasklist.html", context)

def CreateTask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():            
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Task Created Successfully !!")
            return redirect('view_task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def TaskDetails(request, task_id):
    task = get_object_or_404(Task, id= task_id, owner = request.user)
    return render(request, 'task_details.html', {'task' : task})

@login_required
def UpdateTask(request, task_id):
    task = Task.objects.get(id = task_id)
    form = TaskForm(instance= task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance= task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Updated Successfully !!")
            return redirect('view_task_list')
    return render(request, 'create_task.html' , {'form': form, 'edit': True})

@login_required
def DeleteTask(request, task_id):
    task = get_object_or_404(Task, id= task_id, owner = request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task Deleted Succesfully !!")
        return redirect("view_task_list")
    return render(request, 'confirm_delete.html', {'task': task})

@login_required
def TaskMarkComplete(request, task_id):
    task = get_object_or_404(Task, id= task_id, owner = request.user)
    task.status = 'complete'
    task.save()
    messages.success(request, "Task Mark Completed !!")
    return redirect("view_task_list")

def register(request):
    if request.method == "POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            owner = authenticate(username = username, password= password)
            login(request, owner)
            messages.success(request, "Registration Complete !!")
            return redirect('view_task_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def ProfileView(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your profile has been Updated !!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm( instance=profile)
    return render(request, 'profile.html', {'user_form':user_form, 'profile_form':profile_form})