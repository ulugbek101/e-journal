from datetime import date
from .models import Lesson

def validate_lesson_day(lesson: Lesson) -> True | False:
    """
        Returns whether today is the lesson's day or not
    """
    # lesson.lesson_days # "1,3,5" => [1, 3, 5]
    convert_days = map(lambda day: int(day), lesson.lesson_days.split(","))
    lesson_days = list(convert_days)
    today = date.today().weekday + 1

    return today in lesson_days


