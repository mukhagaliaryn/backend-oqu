from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.platform.workspace.services.course import get_lesson_components, generate_test_results, handle_start_lesson, \
    handle_finish_lesson_content, handle_finish_test, handle_finish_lesson
from core.models import UserCourse, UserChapter, UserLesson


def get_previous_and_next_user_lessons(user_lessons, current_user_lesson):
    sorted_lessons = sorted(user_lessons, key=lambda ul: (
        ul.lesson.chapter.order, ul.lesson.order
    ))
    prev_lesson = next_lesson = None

    for idx, ul in enumerate(sorted_lessons):
        if ul.pk == current_user_lesson.pk:
            if idx > 0:
                prev_lesson = sorted_lessons[idx - 1]
            if idx < len(sorted_lessons) - 1:
                next_lesson = sorted_lessons[idx + 1]
            break
    return prev_lesson, next_lesson


# User course lesson page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def user_course_lesson_view(request, user_course_pk, user_chapter_pk, user_lesson_pk):
    user = request.user
    user_course = get_object_or_404(UserCourse, pk=user_course_pk, user=user)
    user_chapter = get_object_or_404(UserChapter, pk=user_chapter_pk, user=user)
    user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk, user=user)
    lesson = user_lesson.lesson

    user_chapters = UserChapter.objects.filter(user_course=user_course)
    user_lessons = UserLesson.objects.filter(user_course=user_course).select_related('lesson__chapter')
    user_lessons_by_chapter = defaultdict(list)
    for ul in user_lessons:
        user_lessons_by_chapter[ul.lesson.chapter_id].append(ul)

    # GET actions
    section = request.GET.get('section', 'text')  # Default is text
    has_text, has_video, has_test, user_text, user_video, user_test = get_lesson_components(user, user_lesson, lesson)
    test_results = generate_test_results(user_test)
    prev_lesson, next_lesson = get_previous_and_next_user_lessons(user_lessons, user_lesson)
    can_access_next = user_lesson.is_completed

    # POST actions
    action = request.POST.get('action')
    if request.method == 'POST':
        if action == 'start_lesson':
            return handle_start_lesson(request, user_course, user_chapter, user_lesson)
        elif action == 'finish_text':
            return handle_finish_lesson_content(request, 'text', user_course, user_chapter, user_lesson)
        elif action == 'finish_video':
            return handle_finish_lesson_content(request, 'video', user_course, user_chapter, user_lesson)
        elif action == 'finish_test':
            return handle_finish_test(request, user_course, user_chapter, user_lesson)
        elif action == 'finish_lesson':
            return handle_finish_lesson(request, user_course, user_chapter, user_lesson, user_text, user_video, user_test, user_lessons)

    # Context data
    # ------------------------------------------------------------------------------------------------------------------
    context = {
        'user_course': user_course,
        'user_chapter': user_chapter,
        'user_lesson': user_lesson,
        'user_chapters': user_chapters,
        'user_lessons_by_chapter': user_lessons_by_chapter,

        'section': section,
        'user_text': user_text,
        'user_video': user_video,
        'user_test': user_test,

        'test_results': test_results,
        'total_questions': len(test_results),
        'correct_questions': sum(1 for r in test_results if r['is_correct']),

        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'can_access_next': can_access_next
    }
    return render(request, 'app/platform/user_course/lesson/page.html', context)

