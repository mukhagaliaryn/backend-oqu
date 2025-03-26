import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from core.models import User


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar
            if old_avatar and instance.avatar != old_avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)  # Файлды жою
        except User.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)