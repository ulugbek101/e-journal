import datetime
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from app_users.models import Class, ClassRoomTeacher, Teacher, Lesson, Student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import forms
from app_users.models import Homework, Parent
from app_users.forms import HomeworkForm


class MyClassDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'class_object'

    def get_object(self, queryset=None):
        classes_list = Class.objects.filter(class_room_teacher=self.request.user)
        if classes_list.count() < 1:
            class_object = None
        else:
            class_object = classes_list[0]
        return class_object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = Paginator(object_list=Student.objects.filter(student_class=self.get_object()), per_page=30)
        page = self.request.GET.get('page') if self.request.GET.get('page') else 1

        try:
            page_obj = pagination.page(page)
        except (EmptyPage, PageNotAnInteger):
            page_obj = pagination.page(pagination.num_pages)


        left_index = page_obj.number - 2
        right_index = page_obj.number + 2

        if left_index - 2 < 1:
            left_index = 1
            right_index = left_index + 4

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages
            left_index = 1
            if right_index - 4 > 0:
                left_index = right_index - 4

        context['class_students'] = page_obj.object_list
        context['page_range'] = range(left_index, right_index + 1)
        context['page_obj'] = page_obj
        return context


    template_name = "app_main/my_class.html"
    extra_context = {
        "my_class": True
    }


class ChatWithParent(LoginRequiredMixin, DetailView):
    template_name = 'app_main/chat.html'
    model = Parent

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        # TODO: Complete Chat Room with parent
        # for class_room in Class.objects.all():
        #     if class_room.class_room_teacher == self.get_queryset()[0].class_room_teacher:
        #         context['class_object'] = class_room
        return context


class ClassList(LoginRequiredMixin, ListView):
    template_name = 'app_main/classes.html'
    extra_context = {
        'classes': True,
    }

    def get_queryset(self):
        return Class.objects.filter(subject_teacher=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated: return redirect('login')
            
        if self.request.user.get_role == "Class room teacher":
            return redirect("my_class")
        return super().dispatch(request, *args, **kwargs)


class ClassCreate(LoginRequiredMixin, CreateView):
    model = Class
    form_class = forms.ClassForm
    template_name = 'form.html'
    extra_context = {
        'btn_text': 'Create class',
        'title': 'New class'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            class_room_teacher = ClassRoomTeacher.objects.get(id=request.POST.get('class_room_teacher'))
            teacher = Teacher.objects.get(id=request.user.id)
            new_class = Class.objects.create(
                name=request.POST.get('name'),
                class_room_teacher=class_room_teacher
            )
            new_class.subject_teacher.add(teacher)
            new_class.save()

            return redirect('classes')

        return super().dispatch(request, *args, **kwargs)


class ClassDetail(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'app_main/class_detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons_list'] = self.object.lesson_set.filter(date__gte=date.today()).order_by('date', 'name')
        return context


class LessonCreate(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = 'app_main/lesson_create_form.html'
    form_class = forms.LessonForm
    extra_context = {
        'btn_text': 'Create lesson',
        'title': 'New lesson',
        'today': date.today().strftime("%Y-%m-%d")  # 2022-12-02
    }

    def form_valid(self, form):
        lesson_name = self.request.POST.get('name')
        lesson_date = self.request.POST.get('date')
        lesson_class_id = self.request.GET.get('from_class')

        new_lesson = Lesson.objects.create(
            name=lesson_name,
            date=lesson_date,
            class_object=Class.objects.get(id=lesson_class_id),
            subject_teacher=Teacher.objects.get(id=self.request.user.id),
        )
        new_lesson.save()
        return redirect('class', id=lesson_class_id)


class LessonDetail(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'app_main/lesson_detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = []
        for student in Student.objects.filter(student_class=self.get_object().class_object):
            is_absent = False
            
            if student.attendance_set.filter(lesson=self.get_object()).count() == 0:
                is_absent = 'Not set'

            elif student.attendance_set.filter(lesson=self.get_object())[0].is_absent == True:
                is_absent = True
                
            students.append({
                'id': student.id,
                'full_name': student.full_name,
                'is_absent': is_absent,
                'grades': student.grade_set.filter(lesson=self.get_object()),
            })
        
        # pagination = Paginator(object_list=students, per_page=1)
        # page = self.request.GET.get('page') if self.request.GET.get('page') else 1
        # context['class_object'] = self.get_object().class_object

        # try:
        #     page_obj = pagination.page(page)
        # except (EmptyPage, PageNotAnInteger):
        #     page_obj = pagination.page(pagination.num_pages)

        
        # left_index = page_obj.number - 2
        # right_index = page_obj.number + 2

        # if left_index - 2 < 1:
        #     left_index = 1
        #     right_index = left_index + 4

        # if right_index > page_obj.paginator.num_pages:
        #     right_index = page_obj.paginator.num_pages
        #     left_index = 1
        #     if right_index - 4 > 0:
                # left_index = right_index - 4

        context['students'] = students # page_obj.object_list
        # context['page_range'] = range(left_index, right_index + 1)
        # context['page_obj'] = page_obj
        context['class_object'] = Class.objects.get(class_room_teacher=self.request.user)
        return context


class ClassLessonsList(LoginRequiredMixin, ListView):
    template_name = 'app_main/class_lessons.html'
    extra_context = {
        'lessons': True,
    }
    paginate_by = 10
    paginator_class = Paginator

    def get_queryset(self):
        class_object = Class.objects.get(id=self.kwargs.get('id'))
        lessons = Lesson.objects.filter(class_object=class_object).filter(
            date__gte=date.today() - datetime.timedelta(days=7)).order_by('date', 'name')
        return lessons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']

        left_index = page_obj.number - 2
        right_index = page_obj.number + 2

        if left_index - 2 < 1:
            left_index = 1
            right_index = left_index + 4

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages
            left_index = 1
            if right_index - 4 > 0:
                left_index = right_index - 4

        context['page_range'] = range(left_index, right_index + 1)
        context['class_object'] = Class.objects.get(id=self.kwargs.get('id'))
        return context


class HomeworkCreate(LoginRequiredMixin, CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'form.html'
    extra_context = {
        'btn_text': 'Create homework',
        'title': 'New homework',
    }

    def form_valid(self, form):
        lesson = Lesson.objects.get(id=self.kwargs.get('id'))
        hw = form.save(commit=False)
        hw.lesson =lesson
        hw.save()
        return redirect('class_lessons', id = lesson.class_object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = Lesson.objects.get(id=self.kwargs.get('id'))
        context['class_object'] = lesson.class_object
        return context


class HomeworkUpdate(LoginRequiredMixin, UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'form.html'
    pk_url_kwarg = 'id'
    extra_context = {
        'btn_text': 'Update homework',
        'title': 'Update homework',
    }

    def get_success_url(self):
        return reverse('class_lessons', kwargs={'id': self.get_object().lesson.class_object.id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = Lesson.objects.get(id=self.kwargs.get('id'))
        context['class_object'] = lesson.class_object
        return context


class HomeworkDelete(LoginRequiredMixin, DeleteView):
    model = Homework
    pk_url_kwarg = 'id'
    template_name = 'delete.html'
    extra_context = {
        'title': 'Delete homework for',
        'description': 'Are you sure to delete this homework ?',
        'btn_text': 'Yes, I\'m 100% sure !',
    }

    def get_success_url(self):
        class_object = self.get_object().lesson.class_object
        return reverse('class_lessons', kwargs={'id': class_object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_object = self.get_object().lesson.class_object
        context['class_object'] = class_object
        context['deleting_object'] = f'\"{Lesson.objects.get(id=self.kwargs.get("lid")).name}\"'
        return context

