from django import forms
from .models import Homework, ClassRoomTeacher
from ckeditor.widgets import CKEditorWidget


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['body']
        widgets = {
            'body': CKEditorWidget(),
        }


class ClassRoomTeacherForm(forms.ModelForm):
    class Meta:
        model = ClassRoomTeacher
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 outline-0 border border-slate-500 rounded'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 outline-0 border border-slate-500 rounded'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 outline-0 border border-slate-500 rounded'
            }),
        }
