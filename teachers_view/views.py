
from django.shortcuts import render

from django.views import View

from  .forms import CreateLessonForm, LoginForm, SettingsForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required(login_url="/teacher/login/")
def hello(request):
    return render(request, 'dashboard.html')

@login_required(login_url="/teacher/login/")
def edit_lesson(request):
    form = CreateLessonForm()

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base.html')
    
    context = {'form': form}
    return render(request, 'edit_lesson.html', context)

@login_required(login_url="/teacher/login/")
def create_lesson(request):
    form = CreateLessonForm()

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base.html')
    
    context = {'form': form}
    return render(request, 'create_lesson.html', context)

@login_required(login_url="/teacher/login/")
def settings_page(request):
    if request.method == 'POST':
        form = SettingsForm()
        user = request.user
        form = SettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, "Settings updated successfully")
            return render(request, 'settings.html')
    else:
        user = request.user
        form = SettingsForm(instance=user)
        return render(request, 'settings.html', {'form': form})


def login_page(request):
    form = LoginForm()
    user = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to dashboard
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    elif request.method == 'GET':
        return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html')
            

