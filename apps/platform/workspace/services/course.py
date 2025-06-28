from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from core.models import UserVideo, UserText, UserTest, UserAnswer


# user_course_lesson controller
# ----------------------------------------------------------------------------------------------------------------------
def get_lesson_components(user, user_lesson, lesson):
    has_text = hasattr(lesson, 'text')
    has_video = hasattr(lesson, 'video')
    has_test = hasattr(lesson, 'test')

    user_text = UserText.objects.filter(user=user, user_lesson=user_lesson).first() if has_text else None
    user_video = UserVideo.objects.filter(user=user, user_lesson=user_lesson).first() if has_video else None
    user_test = UserTest.objects.filter(user=user, user_lesson=user_lesson).first() if has_test else None

    return has_text, has_video, has_test, user_text, user_video, user_test


def generate_test_results(user_test):
    results = []
    if user_test and user_test.is_completed:
        for ua in user_test.user_answers.select_related('question').prefetch_related(
                'selected_answers', 'question__answers'
        ):
            selected_ids = set(ua.selected_answers.values_list('id', flat=True))
            correct_ids = set(ua.question.answers.filter(is_correct=True).values_list('id', flat=True))
            results.append({
                'question': ua.question,
                'user_answers': ua.selected_answers.all(),
                'correct_answers': ua.question.answers.filter(is_correct=True),
                'all_answers': ua.question.answers.all(),
                'is_correct': selected_ids == correct_ids,
            })
    return results


def handle_start_lesson(request, user_course, user_chapter, user_lesson):
    has_text, has_video, has_test, *args = get_lesson_components(request.user, user_lesson, user_lesson.lesson)

    if not any([has_text, has_video, has_test]):
        messages.error(request, _('This lesson has no content to start.'))
        return redirect(request.path)

    if user_lesson.status == 'no-started':
        user_lesson.status = 'in-progress'
        user_lesson.save()

    if has_video:
        UserVideo.objects.get_or_create(
            user=request.user, user_lesson=user_lesson, video=user_lesson.lesson.video
        )
    if has_text:
        UserText.objects.get_or_create(
            user=request.user, user_lesson=user_lesson, text=user_lesson.lesson.text
        )
    if has_test:
        user_test, created = UserTest.objects.get_or_create(
            user=request.user, user_lesson=user_lesson, test=user_lesson.lesson.test
        )
        for question in user_test.test.questions.all():
            UserAnswer.objects.get_or_create(user=request.user, user_test=user_test, question=question)

    messages.success(request, _('This lesson started'))
    return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)


def handle_finish_lesson_content(request, content_type, user_course, user_chapter, user_lesson):
    if content_type == 'text':
        user_text = UserText.objects.filter(
            user=request.user, user_lesson=user_lesson, text=user_lesson.lesson.text
        ).first()
        if user_text and not user_text.is_completed:
            user_text.is_completed = True
            user_text.score = 100
            user_text.save()
            if hasattr(user_lesson.lesson, 'video'):
                url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])
                return redirect(f'{url}?section=video')
        else:
            messages.info(request, _('Text content already finished'))

    elif content_type == 'video':
        user_video = UserVideo.objects.filter(
            user=request.user, user_lesson=user_lesson, video=user_lesson.lesson.video
        ).first()
        if user_video and not user_video.is_completed:
            user_video.is_completed = True
            user_video.score = 100
            user_video.save()
            if hasattr(user_lesson.lesson, 'test'):
                url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])
                return redirect(f'{url}?section=test')
        else:
            messages.info(request, _('Video already finished'))

    return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)


def handle_finish_test(request, user_course, user_chapter, user_lesson):
    user_test = UserTest.objects.filter(
        user=request.user, user_lesson=user_lesson, test=user_lesson.lesson.test
    ).first()
    if user_test and not user_test.is_completed:
        for question in user_lesson.lesson.test.questions.all():
            answer_ids = request.POST.getlist(f'test-{question.id}')
            if not answer_ids:
                continue
            user_answer = user_test.user_answers.filter(question=question).first()
            if user_answer:
                user_answer.selected_answers.set(answer_ids)
                user_answer.save()

        total_questions = user_lesson.lesson.test.questions.count()
        correct_answers = sum(
            1 for ua in user_test.user_answers.all()
            if set(ua.selected_answers.values_list('pk', flat=True)) ==
            set(ua.question.answers.filter(is_correct=True).values_list('pk', flat=True))
        )

        score = (correct_answers / total_questions) * 100 if total_questions else 0
        user_test.score = round(score, 2)
        user_test.is_completed = True
        user_test.save()

        url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])
        return redirect(f'{url}?section=test')
    else:
        messages.info(request, _('Test already finished'))
    return redirect('user_course_lesson', user_lesson.user_course.pk, user_lesson.user_chapter.pk, user_lesson.pk)


def handle_finish_lesson(request, user_course, user_chapter, user_lesson, user_text, user_video, user_test, user_lessons):
    lesson = user_lesson.lesson
    scores = []
    expected = []
    completed = []

    if hasattr(lesson, 'text'):
        expected.append('text')
        if user_text and user_text.is_completed:
            completed.append('text')
            scores.append(user_text.score)
        else:
            messages.warning(request, _('Text not completed.'))

    if hasattr(lesson, 'video'):
        expected.append('video')
        if user_video and user_video.is_completed:
            completed.append('video')
            scores.append(user_video.score)
        else:
            messages.warning(request, _('Video not completed.'))

    if hasattr(lesson, 'test'):
        expected.append('test')
        if user_test and user_test.is_completed:
            completed.append('test')
            scores.append(user_test.score)
        else:
            messages.warning(request, _('Test not completed.'))

    if set(completed) == set(expected):
        user_lesson.status = 'finished'
        user_lesson.is_completed = True
        user_lesson.score = round(sum(scores) / len(scores), 2) if scores else 0
        user_lesson.save()

        total = user_lessons.count()
        completed_score = sum(ul.score for ul in user_lessons)
        user_course.score = round(completed_score / total, 2) if total else 0
        user_course.is_completed = all(ul.is_completed for ul in user_lessons)
        user_course.save()

        messages.success(request, _('Lesson completed successfully.'))
    else:
        messages.warning(request, _('Not all required lesson parts completed.'))

    return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)
