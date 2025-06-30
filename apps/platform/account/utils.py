from functools import wraps
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


def throttle_post(cooldown=1, time_field='last_profile_update', message=None, redirect_url=None, instance='user'):
    """
    Декоратор: POST жіберуді N минут сайын бір ретке шектеу.
    :param cooldown: минут саны
    :param time_field: уақыт сақталған өріс атауы (мысалы, 'last_account_update')
    :param message: хабарлама (None болса, default msg болады)
    :param redirect_url: қай бетке қайта бағыттау (None болса, request.path)
    :param instance: уақыт өрісін қай объектен іздеу ('user', 'user.account' сияқты)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                try:
                    obj = request
                    for attr in instance.split('.'):
                        obj = getattr(obj, attr)
                except AttributeError:
                    return view_func(request, *args, **kwargs)

                cooldown_minutes = timedelta(minutes=cooldown)
                now = timezone.now()
                last_time = getattr(obj, time_field, None)

                if last_time and now - last_time < cooldown_minutes:
                    wait_sec = int((cooldown_minutes - (now - last_time)).total_seconds())
                    wait_min = max(1, wait_sec // 60)
                    msg = message or _('Wait %(minutes)d minutes for forwarding') % {'minutes': wait_min}
                    messages.error(request, msg)
                    return redirect(redirect_url or request.path)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
