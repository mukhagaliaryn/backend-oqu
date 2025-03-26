from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import UserCourse, UserChapter, UserLesson


# User course lesson page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def user_course_lesson(request, user_course_pk, user_chapter_pk, user_lesson_pk):
    user = request.user
    user_course = get_object_or_404(UserCourse, pk=user_course_pk, user=user)
    user_chapter = get_object_or_404(UserChapter, pk=user_chapter_pk, user=user)
    user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk, user=user)

    user_chapters = UserChapter.objects.filter(user_course=user_course)
    context = {
        'user_course': user_course,
        'user_chapter': user_chapter,
        'user_lesson': user_lesson,

        'user_chapters': user_chapters
    }
    return render(request, 'src/pages/user_course/lesson/index.html', context)
