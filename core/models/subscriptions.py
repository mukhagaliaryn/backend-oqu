from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from core.models import User


# Subscription plan model
# ----------------------------------------------------------------------------------------------------------------------
# Subscription
class Subscription(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2, default=0.00)
    duration_days = models.PositiveIntegerField(_('Duration days'), null=True, blank=True)
    is_default = models.BooleanField(_('Is default'), default=False)
    is_unlimited = models.BooleanField(_('Is unlimited'), default=False)
    is_active = models.BooleanField(_('Is active'), default=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            Subscription.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ('order', )


# UserSubscription
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription', verbose_name=_('User'))
    plan = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, related_name='user_subscriptions',
        null=True, verbose_name=_('Plan'))
    start_date = models.DateTimeField(_('Start date'), auto_now_add=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    last_updated = models.DateTimeField(_('Last update'), auto_now=True)

    def save(self, *args, **kwargs):
        if self.plan and self.plan.is_default:
            self.end_date = None
        elif self.plan:
            self.end_date = now() + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.plan.name if self.plan else "No Plan"}'

    class Meta:
        verbose_name = _('User subscription')
        verbose_name_plural = _('User subscriptions')


# UserPayment
class UserPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    plan = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, verbose_name=_('Plan'))
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(_('Payment date'), auto_now_add=True)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(_('Admin note'), blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.amount} ({self.status})'

    class Meta:
        verbose_name = _('User payment')
        verbose_name_plural = _('User payments')
