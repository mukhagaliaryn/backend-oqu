from collections import defaultdict
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from core.models import UserCourse, UserChapter, UserLesson, UserVideo, UserText, UserTest, UserAnswer


# User course lesson page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def user_course_lesson_view(request, user_course_pk, user_chapter_pk, user_lesson_pk):
    # Get all queryset
    # ------------------------------------------------------------------------------------------------------------------
    user = request.user
    user_course = get_object_or_404(UserCourse, pk=user_course_pk, user=user)
    user_chapter = get_object_or_404(UserChapter, pk=user_chapter_pk, user=user)
    user_lesson = get_object_or_404(UserLesson, pk=user_lesson_pk, user=user)
    lesson = user_lesson.lesson

    user_chapters = UserChapter.objects.filter(user_course=user_course)
    user_lessons = UserLesson.objects.filter(user_course=user_course).select_related('lesson__chapter')
    user_lessons_by_chapter = defaultdict(list)
    for ul in user_lessons:
        chapter_id = ul.lesson.chapter_id
        user_lessons_by_chapter[chapter_id].append(ul)

    # GET actions
    # ------------------------------------------------------------------------------------------------------------------
    # Section control (?section=video/text/test)
    section = request.GET.get('section', 'text')  # default is text
    user_text = user_video = user_test = None

    if hasattr(lesson, 'video'):
        user_video = UserVideo.objects.filter(user=user, user_lesson=user_lesson).first()

    if hasattr(lesson, 'text'):
        user_text = UserText.objects.filter(user=user, user_lesson=user_lesson).first()

    if hasattr(lesson, 'test'):
        user_test = UserTest.objects.filter(user=user, user_lesson=user_lesson).first()

    test_results = []
    if user_test and user_test.is_completed:
        for ua in user_test.user_answers.select_related('question').prefetch_related(
                'selected_answers', 'question__answers'
        ):
            selected_ids = set(ua.selected_answers.values_list('id', flat=True))
            correct_ids = set(ua.question.answers.filter(is_correct=True).values_list('id', flat=True))
            test_results.append({
                'question': ua.question,
                'user_answers': ua.selected_answers.all(),
                'correct_answers': ua.question.answers.filter(is_correct=True),
                'all_answers': ua.question.answers.all(),
                'is_correct': selected_ids == correct_ids,
            })
    total_questions = len(test_results)
    correct_answers = sum(1 for r in test_results if r['is_correct'])

    # POST actions
    # ------------------------------------------------------------------------------------------------------------------
    # Start lesson action
    if request.method == 'POST' and request.POST.get('action') == 'start_lesson':
        has_video = hasattr(lesson, 'video')
        has_text = hasattr(lesson, 'text')
        has_test = hasattr(lesson, 'test')

        if not any([has_video, has_text, has_test]):
            messages.error(request, _('This lesson has no content to start.'))
            return redirect(request.path)

        if user_lesson.status == 'no-started':
            user_lesson.status = 'in-progress'
            user_lesson.save()

        if has_video:
            UserVideo.objects.get_or_create(user=user, user_lesson=user_lesson, video=lesson.video)

        if has_text:
            UserText.objects.get_or_create(user=user, user_lesson=user_lesson, text=lesson.text)

        if has_test:
            user_test, created = UserTest.objects.get_or_create(user=user, user_lesson=user_lesson, test=lesson.test)
            for question in user_test.test.questions.all():
                UserAnswer.objects.get_or_create(user=user_test.user, user_test=user_test, question=question)

        messages.success(request, _('This lesson started'))
        return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)

    # Finish text action
    if request.method == 'POST' and request.POST.get('action') == 'finish_text':
        if hasattr(lesson, 'text'):
            user_text = UserText.objects.filter(user=user, user_lesson=user_lesson, text=lesson.text).first()
            if user_text and not user_text.is_completed:
                user_text.is_completed = True
                user_text.score = 100
                user_text.save()
                messages.success(request, _('Text content finished'))
                url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])

                if hasattr(lesson, 'video'):
                    return redirect(f'{url}?section=video')
                elif hasattr(lesson, 'test'):
                    return redirect(f'{url}?section=test')
            else:
                messages.info(request, _('Text content already finished'))
            return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)

    # Finish video action
    if request.method == 'POST' and request.POST.get('action') == 'finish_video':
        if hasattr(lesson, 'video'):
            user_video = UserVideo.objects.filter(user=user, user_lesson=user_lesson, video=lesson.video).first()
            if user_video and not user_video.is_completed:
                user_video.is_completed = True
                user_video.score = 100
                user_video.save()
                messages.success(request, _('Video finished'))
                url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])

                if hasattr(lesson, 'test'):
                    return redirect(f'{url}?section=test')
            else:
                messages.info(request, _('Video already finished'))
            return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)

    # Complete/finish test action
    if request.method == 'POST' and request.POST.get('action') == 'finish_test':
        if hasattr(lesson, 'test'):
            user_test = UserTest.objects.filter(user=user, user_lesson=user_lesson, test=lesson.test).first()

            if user_test and not user_test.is_completed:
                for question in lesson.test.questions.all():
                    answer_ids = request.POST.getlist(f'test-{question.id}')
                    if not answer_ids:
                        continue

                    user_answer = user_test.user_answers.filter(question=question).first()
                    if user_answer:
                        user_answer.selected_answers.set(answer_ids)
                        user_answer.save()

                total_questions = lesson.test.questions.count()
                correct_answers = 0

                for user_answer in user_test.user_answers.all():
                    selected = set(user_answer.selected_answers.values_list('pk', flat=True))
                    correct = set(user_answer.question.answers.filter(is_correct=True).values_list('pk', flat=True))
                    if selected == correct:
                        correct_answers += 1

                score = (correct_answers / total_questions) * 100 if total_questions else 0
                user_test.score = round(score, 2)
                user_test.is_completed = True
                user_test.save()

                messages.success(request, _('Test finished. Score: {}%').format(user_test.score))
                url = reverse('user_course_lesson', args=[user_course.pk, user_chapter.pk, user_lesson.pk])
                return redirect(f'{url}?section=test')
            else:
                messages.info(request, _('Test already finished'))
            return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)

    # Finish lesson
    if request.method == 'POST' and request.POST.get('action') == 'finish_lesson':
        completed_items = []
        scores = []
        expected_parts = []

        if hasattr(lesson, 'text'):
            expected_parts.append('text')
        if hasattr(lesson, 'video'):
            expected_parts.append('video')
        if hasattr(lesson, 'test'):
            expected_parts.append('test')

        # Text
        if hasattr(lesson, 'text'):
            if user_text and user_text.is_completed:
                completed_items.append('text')
                scores.append(user_text.score)
            else:
                messages.warning(request, _('Text not completed.'))

        # Video
        if hasattr(lesson, 'video'):
            if user_video and user_video.is_completed:
                completed_items.append('video')
                scores.append(user_video.score)
            else:
                messages.warning(request, _('Video not completed.'))

        # Test
        if hasattr(lesson, 'test'):
            if user_test and user_test.is_completed:
                completed_items.append('test')
                scores.append(user_test.score)
            else:
                messages.warning(request, _('Test not completed.'))

        if set(completed_items) == set(expected_parts):
            average_score = sum(scores) / len(scores) if scores else 0
            user_lesson.status = 'finished'
            user_lesson.is_completed = True
            user_lesson.score = round(average_score, 2)
            user_lesson.save()
            messages.success(request, _('Lesson completed successfully.'))

            # Course progress
            total_lessons = user_lessons.count()
            completed_score = sum([
                ul.score for ul in user_lessons
                if ul.is_completed and ul.score is not None
            ])
            user_course.score = round(completed_score / total_lessons, 2) if total_lessons > 0 else 0
            user_course.is_completed = all(ul.is_completed for ul in user_lessons)
            user_course.save()
        else:
            messages.warning(request, _('Not all required lesson parts completed.'))

        return redirect('user_course_lesson', user_course.pk, user_chapter.pk, user_lesson.pk)

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
        'total_questions': total_questions,
        'correct_questions': correct_answers,
    }
    return render(request, 'src/pages/user_course/lesson/index.html', context)
