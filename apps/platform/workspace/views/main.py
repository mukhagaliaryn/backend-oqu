from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from core.models import Category, Course, UserCourse, UserChapter, UserLesson, UserVideo, UserText, UserTest


# Workspace page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def workspace(request):
    user = request.user
    user_courses = UserCourse.objects.select_related('course').filter(user=user)

    first_lessons = {}
    first_chapters = {}

    for uc in user_courses:
        user_lessons = uc.user_lessons.select_related('lesson').order_by('lesson__order')
        user_chapters = uc.user_chapters.select_related('chapter').order_by('chapter__order')

        if user_lessons.exists():
            first_lessons[uc.id] = user_lessons.first().id
        if user_chapters.exists():
            first_chapters[uc.id] = user_chapters.first().id

    completed_lessons_count = UserLesson.objects.filter(user_course__in=user_courses, is_completed=True).count()
    context = {
        'user_courses': user_courses,
        'first_lesson_ids': first_lessons,
        'first_chapter_ids': first_chapters,
        'completed_lessons_count': completed_lessons_count
    }
    return render(request, 'app/platform/index.html', context)


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
    return render(request, 'app/platform/resources.html', context)


# Course page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def course_detail(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    user_course_ids = set(
        UserCourse.objects.filter(user=user).values_list('course_id', flat=True)
    )
    user_course = UserCourse.objects.filter(user=user, course=course).first()
    first_user_chapter = None
    first_user_lesson = None

    if user_course:
        first_user_chapter = user_course.user_chapters.select_related('chapter').order_by('chapter__order').first()
        first_user_lesson = user_course.user_lessons.select_related('lesson').order_by('lesson__order').first()

    context = {
        'course': course,
        'user_course_ids': user_course_ids,
        'user_course': user_course,
        'first_user_chapter': first_user_chapter,
        'first_user_lesson': first_user_lesson
    }
    return render(request, 'pages/course/index.html', context)


# POST actions
# ----------------------------------------------------------------------------------------------------------------------
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

    for chapter in chapters:
        UserChapter.objects.get_or_create(user=user, chapter=chapter, user_course=user_course)

    for lesson in lessons:
        user_lesson, created = UserLesson.objects.get_or_create(user=user, lesson=lesson, user_course=user_course)

        if hasattr(lesson, 'video'):
            UserVideo.objects.get_or_create(user=user, user_lesson=user_lesson, video=lesson.video)

        if hasattr(lesson, 'text'):
            UserText.objects.get_or_create(user=user, user_lesson=user_lesson, text=lesson.text)

        if hasattr(lesson, 'test'):
            UserTest.objects.get_or_create(user=user, user_lesson=user_lesson, test=lesson.test)

    messages.success(request, _('You have successfully enrolled in the course'))
    return redirect('workspace')
