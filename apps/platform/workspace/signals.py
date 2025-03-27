from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.platform.workspace.utils import update_user_progress_for_course
from core.models import Lesson


@receiver(post_save, sender=Lesson)
def auto_update_user_progress(sender, instance, created, **kwargs):
    update_user_progress_for_course(instance.course)