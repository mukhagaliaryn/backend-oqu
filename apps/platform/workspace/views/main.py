from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from core.models import Category, Course, UserCourse, UserChapter, UserLesson, Chapter


# Workspace page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def workspace(request):
    user = request.user
    user_courses = UserCourse.objects.select_related('course').filter(user=user)

    user_chapters = UserChapter.objects.filter(user_course__in=user_courses).values('id', 'user_course_id')
    user_lessons = UserLesson.objects.filter(user_course__in=user_courses).values('id', 'user_course_id')
    chapter_map = {}
    lesson_map = {}
    for uc in user_chapters:
        chapter_map[uc['user_course_id']] = uc['id']
    for ul in user_lessons:
        lesson_map[ul['user_course_id']] = ul['id']

    context = {
        'user_courses': user_courses,
        'chapter_map': chapter_map,
        'lesson_map': lesson_map,
    }
    return render(request, 'src/pages/index.html', context)


# Resources page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def resources(request):
    user = request.user
    categories = Category.objects.prefetch_related(
        'sub_categories__sub_courses__authors'
    ).all()

    user_course_ids = set(
        UserCourse.objects.filter(user=user).values_list('course_id', flat=True)
    )
    context = {
        'categories': categories,
        'user_course_ids': user_course_ids
    }
    return render(request, 'src/pages/resources.html', context)


# Course page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def course_detail(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    user_course_ids = set(
        UserCourse.objects.filter(user=user).values_list('course_id', flat=True)
    )
    context = {
        'course': course,
        'user_course_ids': user_course_ids
    }
    return render(request, 'src/pages/course/index.html', context)


# create user course handler
@require_POST
@login_required
def create_user_course_handler(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)

    chapters = course.chapters.all()
    lessons = course.lessons.all()

    if not chapters.exists() or not lessons.exists():
        messages.error(request, _('There is no material in this course'))
        return redirect('resources')

    user_course, created = UserCourse.objects.get_or_create(user=user, course=course)

    # Chapters
    for chapter in chapters:
        UserChapter.objects.get_or_create(user=user, chapter=chapter, user_course=user_course)

    # Lessons
    for lesson in lessons:
        UserLesson.objects.get_or_create(user=user, lesson=lesson, user_course=user_course)

    messages.success(request, _('You have successfully enrolled in the course'))
    return redirect('workspace')


