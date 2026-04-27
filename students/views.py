from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .models import Student, Attendance
from .forms import StudentForm, AttendanceForm


# =========================
# AUTHENTICATION
# =========================

def register(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'students/register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'students/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    total = Student.objects.count()
    return render(request, 'students/dashboard.html', {'total': total})


# =========================
# STUDENTS
# =========================

@login_required
def student_list(request):
    q = request.GET.get('q')

    if q:
        students = Student.objects.filter(name__icontains=q)
    else:
        students = Student.objects.all()

    return render(request, 'students/list.html', {'students': students})


@login_required
def add_student(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        student.save()

        messages.success(request, "✅ Student added successfully!")
        return redirect('student_list')

    return render(request, 'students/form.html', {'form': form})


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Student updated successfully!")
        return redirect('student_list')

    return render(request, 'students/form.html', {'form': form})


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()

    messages.success(request, "🗑️ Student deleted successfully!")
    return redirect('student_list')


# =========================
# ATTENDANCE
# =========================

@login_required
def attendance_view(request):
    records = Attendance.objects.select_related('student').all()
    form = AttendanceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "📅 Attendance added!")
        return redirect('attendance')

    return render(request, 'students/attendance.html', {
        'records': records,
        'form': form
    })
@login_required
def add_attendance(request):
    form = AttendanceForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "📅 Attendance added!")
        return redirect('attendance')

    return render(request, 'students/attendance_form.html', {'form': form})