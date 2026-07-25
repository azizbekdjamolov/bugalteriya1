from .models import Notification


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {}
    qs = Notification.objects.filter(is_read=False).order_by('-created_at')
    return {
        'unread_notifications': qs[:20],
        'unread_notifications_count': qs.count(),
        'critical_notification': qs.filter(level=Notification.Level.RED).first() or qs.filter(
            level=Notification.Level.ORANGE).first(),
    }
