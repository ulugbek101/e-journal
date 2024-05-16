from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserAccountManager, StudentManager, TeacherManager, ClassRoomTeacherManager, ParentManager

from ckeditor.fields import RichTextField

from app_main.models import Subject


class Class(models.Model):
    name = models.CharField(max_length=10)
    subject_teacher = models.ManyToManyField(
        "Teacher", related_name="subject_teachers")
    class_room_teacher = models.OneToOneField("ClassRoomTeacher", on_delete=models.SET_NULL, null=True,
                                              related_name="class_room_teacher")

    def __str__(self):
        return self.name


class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        PARENT = "PARENT", "Parent"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
        CLASS_ROOM_TEACHER = "CLASS_ROOM_TEACHER", "Class Room Teacher"

    type = models.CharField(max_length=18, choices=Types.choices,
                            # Default user is teacher
                            default=Types.TEACHER)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    # If user if student
    student_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(to="Parent", on_delete=models.SET_NULL, null=True, related_name="parent_students")

    # If user is subject teacher
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # special permission which define that
    # the new user is teacher or student
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_class_room_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = "email"

    # defining the manager for the UserAccount model
    objects = UserAccountManager()

    @property
    def get_role(self):
        return self.type.capitalize().replace("_", " ")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.type or self.type is None:
            self.type = UserAccount.Types.TEACHER
        return super().save(*args, **kwargs)


class Student(UserAccount):
    class Meta:
        proxy = True

    objects = StudentManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.STUDENT
        self.is_student = True
        return super().save(*args, **kwargs)


class Teacher(UserAccount):
    class Meta:
        proxy = True

    objects = TeacherManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.TEACHER
        self.is_teacher = True
        return super().save(*args, **kwargs)


class ClassRoomTeacher(UserAccount):
    class Meta:
        proxy = True

    objects = ClassRoomTeacherManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.CLASS_ROOM_TEACHER
        self.is_class_room_teacher = True
        return super().save(*args, **kwargs)


class Parent(UserAccount):
    class Meta:
        proxy = True

    objects = ParentManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.PARENT
        self.is_parent = True
        return super().save(*args, **kwargs)


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    subject_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    class_object = models.ForeignKey(Class, on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.class_object.name} - {self.subject_teacher.full_name}"


class Homework(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lesson.name} - {self.lesson.date}"


class Attendance(models.Model):
    is_absent = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.full_name} - {self.is_absent}"


class Grade(models.Model):
    class GradeChoices(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
        F = "F", "F"

    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    grade = models.CharField(
        max_length=1, choices=GradeChoices, null=True, blank=True)

    def __str__(self):
        return f"{self.lesson.name} - {self.student.full_name} - {self.grade}"

    class Meta:
        unique_together = (
            ('lesson', 'student'),
        )


class ChatMessage(models.Model):
    # if class_room_teacher is NULL then in frontend we should render "Deleted account" insetead of class_room_teacher.full_name
    class_room_teacher = models.ForeignKey(to=ClassRoomTeacher, on_delete=models.SET_NULL, null=True, related_name='class_room_teacher_messages')
    # if class_room_teacher is NULL then in frontend we should render "Deleted account" insetead of parent.full_name
    parent = models.ForeignKey(to=Parent, on_delete=models.SET_NULL, null=True, related_name='parent_messages')
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_room_teacher.full_name} - {self.parent.full_name}"
