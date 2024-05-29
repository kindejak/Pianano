
from django.shortcuts import render, redirect

from django.views import View

from  .forms import CreateLessonForm, LoginForm, SettingsForm, CreateStudentForm, CreateQuestionForm, MusicLesson, CreateClassForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password

from lessons_api.models import StudentLesson, Student
from django.contrib.auth.models import User





def update_all_streaks():
    students = Student.objects.all()
    for student in students:
        student.update_streak()

@login_required(login_url="/teacher/login/")
def hello(request):
    context = {}
    # get last 5 studentlessons that were finished and belong to the teacher
    students = Student.objects.filter(teacher=request.user)
    student_lessons = []
    for student in students:
        student_lessons += student.studentlesson_set.filter(is_finished=True).order_by('-datetime_finished')
    # sort by date_finished
    student_lessons = sorted(student_lessons, key=lambda x: x.datetime_finished, reverse=True)
    student_lessons = student_lessons[:5]
    context_lessons = []
    for student_lesson in student_lessons:
        student = student_lesson.student
        context_lessons.append({
            'student': student.user.username,
            'avatar_id': student.avatar_id,
            'time_spent': student_lesson.time_spent,
            'finished': student_lesson.datetime_finished,
        })
    context['student_lessons'] = context_lessons

    students = []
    for student in Student.objects.filter(teacher=request.user):
        students.append({
            'username': student.user.username,
            'avatar_id': student.avatar_id,
            'xp': student.xp,
            'streak': student.streak,
        })
    context['students'] = students
    print(context)
    update_all_streaks()
    return render(request, 'dashboard.html', context)


@login_required(login_url="/teacher/login/")
def students(request):
    return render(request, 'students.html')

@login_required(login_url="/teacher/login/")
def create_student(request):
    form = CreateStudentForm()

    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            avatar_id = form.cleaned_data['avatar_id']
            if password1 != password2:
                return render(request, 'create_student.html', {'form': form, 'error': 'Passwords do not match'})
            if User.objects.filter(username=username).exists():
                return render(request, 'create_student.html', {'form': form, 'error': 'Username already exists'})
            if avatar_id < 0 or avatar_id > 8:
                return render(request, 'create_student.html', {'form': form, 'error': 'Invalid avatar id'})
            if validate_password == False:
                return render(request, 'create_student.html', {'form': form, 'error': 'Password is too weak'})
            user = User.objects.create_user(username=username, password=password1)
            student = Student.objects.create(user=user, teacher=request.user, avatar_id=avatar_id)
            return redirect('students')
    return render(request, 'create_student.html', {'form': form})

@login_required(login_url="/teacher/login/")
def create_question(request):
    form = CreateQuestionForm()

    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        teacher = request.user
        form.instance.teacher = teacher
        if form.is_valid():
            form.save()
            return render(request, 'create_question.html', {'form': form, 'success': 'Question created successfully'})
    return render(request, 'create_question.html', {'form': form})


@login_required(login_url="/teacher/login/")
def lesson(request):
    # get all lessons that belong to the teacher
    lessons = request.user.musiclesson_set.all()
    context_lessons = []
    for lesson in lessons:
        context_lessons.append({
            'id': lesson.id,
            'name': lesson.name,
            'xp': lesson.xp,
            'is_public': lesson.is_public,
        }) 
    return render(request, 'lesson.html', {'lessons':context_lessons})

@login_required(login_url="/teacher/login/")
def delete_lesson(request, id=None):
    if id is None:
        return redirect('lessons', {'error': 'Invalid id'})
    if request.user.musiclesson_set.filter(id=id).exists():
        lesson = MusicLesson.objects.get(id=id)
        lesson.delete()
        return redirect('lessons')
    else:
        return redirect('lessons', {'error': 'Invalid id'})

@login_required(login_url="/teacher/login/")
def edit_lesson(request):
    return render(request, 'edit_lesson.html')

@login_required(login_url="/teacher/login/")
def create_lesson(request, id=None):
    form = CreateLessonForm()
    context = {}

    if id is not None and request.method == 'GET':
        lesson = MusicLesson.objects.get(id=id)
        form = CreateLessonForm(instance=lesson)
        context['lesson'] = lesson
        return render(request, 'create_lesson.html', {'form': form})
    
    if id is not None and request.method == 'POST':
        lesson = MusicLesson.objects.get(id=id)
        form = CreateLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lessons')
        else:
            return render(request, 'create_lesson.html', {'form': form, 'error': 'Invalid data'})

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        # set teacher to the current user
        form.instance.teacher = request.user
        if form.is_valid():
            form.save()
            return redirect('lessons')
        else:
            return render(request, 'create_lesson.html',{'form': form, 'error':'Invalid data'} )
    
    return render(request, 'create_lesson.html', {'form': form})



def create_class(request):
    form = CreateClassForm()
    if request.method == 'GET':
        return render(request, 'create_class.html', {'form': form})
    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        # set teacher to the current user
        form.instance.teacher = request.user
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'create_class.html', {'form': form, 'error': 'Invalid data'})
        

@login_required(login_url="/teacher/login/")
def settings_page(request):
    if request.method == 'POST':
        user = request.user
        form = SettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, "Settings updated successfully")
            return render(request, 'settings.html', {'form': form})
    else:
        user = request.user
        form = SettingsForm(instance=user)
        return render(request, 'settings.html', {'form': form})

def delete_account(request):
    user = request.user
    if user.is_authenticated:
        user.delete()
    return redirect('login-page')

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    return render(request, 'login.html', {'form': form})

            

