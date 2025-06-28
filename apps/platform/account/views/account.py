from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.platform.account.forms.account import UserUpdateForm, AccountForm, PasswordChangeForm
from core.models import Subscription, UserPayment


# profile page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile saved'))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'pages/accounts/account/profile.html', context)


# account page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def account(request):
    user = request.user
    user_account = user.account

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()
            messages.success(request, _('Account saved'))
            return redirect('account')
    else:
        form = AccountForm(instance=user_account)

    context = {
        'account': user_account,
        'form': form
    }
    return render(request, 'pages/accounts/account/account.html', context)


# subscriptions page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def subscriptions(request):
    items = Subscription.objects.filter(is_active=True).exclude(user_subscriptions__user=request.user)
    context = {
        'items': items
    }
    return render(request, 'pages/accounts/account/subscriptions.html', context)



# payments page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def payments(request):
    items = UserPayment.objects.filter(user=request.user)
    context = {
        'items': items
    }
    return render(request, 'pages/accounts/account/payments.html', context)



@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password changed'))
            return redirect('account')
        else:
            messages.error(request, _('Failed to change password'))

    form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'pages/accounts/account/password_change.html', context)


# settings page
# ----------------------------------------------------------------------------------------------------------------------
@login_required
def settings(request):
    context = {}
    return render(request, 'pages/accounts/account/settings.html', context)