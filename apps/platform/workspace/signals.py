from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.platform.workspace.utils import update_user_progress_for_course
from core.models import Lesson, Video, UserLesson, UserVideo, Text, UserText, Test, UserTest, Question, UserAnswer


@receiver(post_save, sender=Lesson)
def auto_update_user_progress(sender, instance, created, **kwargs):
    if created:
        update_user_progress_for_course(instance.course)


@receiver(post_save, sender=Video)
def auto_create_user_video(sender, instance, created, **kwargs):
    lesson = instance.lesson
    user_lessons = UserLesson.objects.filter(lesson=lesson)

    for ul in user_lessons:
        UserVideo.objects.get_or_create(user=ul.user, user_lesson=ul, video=instance)


@receiver(post_save, sender=Text)
def auto_create_user_text(sender, instance, created, **kwargs):
    lesson = instance.lesson
    user_lessons = UserLesson.objects.filter(lesson=lesson)

    for ul in user_lessons:
        UserText.objects.get_or_create(user=ul.user, user_lesson=ul, text=instance)


@receiver(post_save, sender=Test)
def auto_create_user_test(sender, instance, created, **kwargs):
    lesson = instance.lesson
    user_lessons = UserLesson.objects.filter(lesson=lesson)

    for ul in user_lessons:
        UserTest.objects.get_or_create(user=ul.user, user_lesson=ul, test=instance)
