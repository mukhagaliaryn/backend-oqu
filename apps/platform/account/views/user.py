from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.platform.account.utils import throttle_post
from core.models import Subscription, UserPayment, Account
from apps.platform.account.forms.user import UserUpdateForm, AccountForm
from django.contrib.auth.forms import PasswordChangeForm


# profile page
# ----------------------------------------------------------------------------------------------------------------------
@throttle_post(cooldown=5)
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if form.has_changed():
                form.save()
                user.last_profile_update = timezone.now()
                user.save(update_fields=['last_profile_update'])
                messages.success(request, _('Profile saved'))
                return redirect('profile')
            else:
                messages.info(request, _('No changes found'))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'app/platform/account/user/profile.html', context)


# account page
# ----------------------------------------------------------------------------------------------------------------------
@throttle_post(cooldown=5, time_field='last_account_update', instance='user.account')
@login_required
def account(request):
    user = request.user
    try:
        user_account = user.account
    except Account.DoesNotExist:
        user_account = Account.objects.create(user=user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user_account)
        if form.is_valid():
            if form.has_changed():
                form.save()
                user_account.last_account_update = timezone.now()
                user_account.save(update_fields=['last_account_update'])
                messages.success(request, _('Account saved'))
                return redirect('account')
            else:
                messages.info(request, _('No changes found'))
            return redirect('account')
    else:
        form = AccountForm(instance=user_account)

    context = {
        'account': user_account,
        'form': form
    }
    return render(request, 'app/platform/account/user/account.html', context)


# subscriptions page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def subscriptions(request):
    items = Subscription.objects.filter(is_active=True).exclude(user_subscriptions__user=request.user)
    context = {
        'items': items
    }
    return render(request, 'app/platform/account/subscriptions.html', context)



# payments page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def payments(request):
    items = UserPayment.objects.filter(user=request.user)
    context = {
        'items': items
    }
    return render(request, 'app/platform/account/payments.html', context)



# password change page
# ----------------------------------------------------------------------------------------------------------------------
@throttle_post(cooldown=5)
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            user.last_profile_update = timezone.now()
            user.save(update_fields=['last_profile_update'])
            messages.success(request, _('Password changed'))
            return redirect('password_change')
        else:
            messages.error(request, _('Failed to change password'))

    form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'app/platform/account/user/password_change.html', context)


# settings page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def settings(request):
    context = {}
    return render(request, 'app/platform/account/user/settings.html', context)
