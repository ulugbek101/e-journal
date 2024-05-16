from django.urls import path
from . import views

urlpatterns = [
    # subject teacher routes
    path('', views.ClassList.as_view(), name='classes'),
    path('create-class/', views.ClassCreate.as_view(), name='create_class'),
    path('create-lesson/', views.LessonCreate.as_view(), name='create_lesson'),
    path('class/<int:id>/', views.ClassDetail.as_view(), name='class'),

    # class room teacher routes
    path('my-class/', views.MyClassDetail.as_view(), name='my_class'),
    path('class-lessons/<int:id>/', views.ClassLessonsList.as_view(), name='class_lessons'),
    path('lesson-detail/<int:id>/', views.LessonDetail.as_view(), name='lesson_detail'),
    path('create-homework/<int:id>/', views.HomeworkCreate.as_view(), name='create_homework'),
    path('update-homework/<int:id>/', views.HomeworkUpdate.as_view(), name='update_homework'),
    path('delete-homework/<int:lid>/<int:id>/', views.HomeworkDelete.as_view(), name='delete_homework'),
    path('chat/', views.ChatWithParent.as_view(), name='chat_with_parent')
]
