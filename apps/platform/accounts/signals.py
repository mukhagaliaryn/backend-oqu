import os
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save, post_delete
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from core.models import User, Account, UserPayment, UserSubscription, Subscription



# Create user account signals
# ----------------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        free_plan = Subscription.objects.filter(is_default=True).first()
        if free_plan:
            end_date = None
            if not free_plan.is_unlimited:
                end_date = now() + timedelta(days=free_plan.duration_days)

            UserSubscription.objects.create(
                user=instance,
                plan=free_plan,
                start_date=now(),
                end_date=end_date,
                is_active=True
            )
        else:
            print('⚠️ Default (free) subscription plan not found!')


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    if hasattr(instance, 'account'):
        instance.account.save()


# Subscription signals
# ----------------------------------------------------------------------------------------------------------------------
@receiver(post_save, sender=UserPayment)
def update_subscription_on_payment(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        user_subscription, created = UserSubscription.objects.get_or_create(user=instance.user)

        user_subscription.plan = instance.plan
        user_subscription.start_date = now()
        user_subscription.end_date = now() + timedelta(days=instance.plan.duration_days)
        user_subscription.is_active = True
        user_subscription.save()


# Manage user avatar signals
# ----------------------------------------------------------------------------------------------------------------------
@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar
            if old_avatar and instance.avatar != old_avatar:
                if default_storage.exists(old_avatar.name):
                    default_storage.delete(old_avatar.name)
        except User.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if default_storage.exists(instance.avatar.name):
            default_storage.delete(instance.avatar.name)
