from administrator.models import Parent, General_notification, Students
from django.shortcuts import get_object_or_404
from django.http import Http404

def dashboard_data(request):
    parent_id = request.session.get("parent_id")
    
    if not parent_id:
        return {
            "my_kid": 0,
            "get_generalp": 0,
            "get_general_infop": [],
            "get_general_tp": 0,
            "get_general_info_tp": [],
            "numbttp": 0
        }
    
    try:
        parent = Parent.objects.get(id=parent_id)
    except Parent.DoesNotExist:
        raise Http404("Parent not found")
    kids_count = Students.objects.filter(student_parent__id=parent_id).count()
    general_notifications_count = General_notification.objects.filter(g_not_audience='General').count()
    parent_notifications_count = General_notification.objects.filter(g_not_audience='Parents').count()
    general_notifications = General_notification.objects.filter(g_not_audience='General')
    parent_notifications = General_notification.objects.filter(g_not_audience='Parents')
    total_notifications_count = general_notifications_count + parent_notifications_count
    
    return {
        "my_kid": kids_count,
        "get_generalp": general_notifications_count,
        "get_general_infop": general_notifications,
        "get_general_tp": parent_notifications_count,
        "get_general_info_tp": parent_notifications,
        "numbttp": total_notifications_count
    }