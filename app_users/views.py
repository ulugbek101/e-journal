import json

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import JsonResponse
from .models import Attendance, Lesson, Student, Class, Grade, ClassRoomTeacher
from .forms import ClassRoomTeacherForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/profile.html'
    extra_context = {
        'profile': True,
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.user.is_class_room_teacher:
            form = ClassRoomTeacherForm(instance=self.request.user)
            context['class_object'] = Class.objects.get(
                class_room_teacher=self.request.user)
            context['form'] = form
            context['user'] = self.request.user
        return context


class LoginUserView(LoginView):
    template_name = 'login.html'


def update_profile_information(request):
    if request.method == 'GET':
        return HttpResponse("Not found")
    
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.save()
    return redirect('profile')


def update_profile_password(request):
    if request.method == 'GET':
        return HttpResponse("Not found")

    if request.POST.get('password1') == request.POST.get('password2'):
        user = request.user
        user.set_password(request.POST.get('password2'))
        user.save()

        login(request, user)
        # TODO: display success message on password change

    else:
        ...
        # TODO: display error message on passwords mismatch

    return redirect('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def update_attendance(request):
    data = json.loads(request.body)
    students = [int(student.get('studentId'))
                for student in data['absentStudents']]
    lesson_id = data['lessonId']

    try:
        lesson = Lesson.objects.get(id=lesson_id)

        for student in Student.objects.all():
            attendance = Attendance(
                is_absent=True if student.id in students else False,
                student=student,
                lesson=lesson,
            )
            attendance.save()

        return JsonResponse("Success", safe=False)
    except:
        return JsonResponse("Error", safe=False)


@csrf_exempt
def update_grades(request):
    # Recieve and deserialize JSON data
    data = json.loads(request.body)

    # Set grade for recieved student
    grades_list = data.get('gradesList')

    for grade_information in grades_list:
        student = Student.objects.get(id=grade_information.get('studentId'))
        lesson = Lesson.objects.get(id=grade_information.get('lessonId'))
        grade = grade_information.get('grade')

        grade = Grade.objects.create(
            student=student,
            lesson=lesson,
            grade=grade
        )
        grade.save()

    return JsonResponse(data="Success", safe=False)
