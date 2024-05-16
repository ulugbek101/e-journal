from django.forms import ModelForm
from app_users.models import Class, Lesson
from django import forms


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'subject_teacher', 'class_room_teacher']
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border border-slate-500 rounded'
            })


        if user and user.is_teacher:
            self.fields.pop('subject_teacher')


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'date']
        # widgets = {
        #     'date': forms.DateField(widget=forms.DateInput())
        # }