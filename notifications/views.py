from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.all()[:200]
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    n = get_object_or_404(Notification, pk=pk)
    n.is_read = True
    n.save(update_fields=['is_read'])
    return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))


@login_required
def mark_all_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))
