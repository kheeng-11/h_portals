from administrator.models import Students, Payment, Assignment, Class,General_notification, Notifications
from django.shortcuts import get_object_or_404
from django.http import Http404


def dashboard_data(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return {
            "payment": 0,
            "assignment": 0,
            "get_generals": 0,
            "get_general_infos": [],
            "get_general_ts": 0,
            "get_general_info_ts": [],
            "numbtts": 0,
            "get_class_ts": 0,
            "get_class_infos": []
        }
    try:
        student = Students.objects.get(id=student_id)
    except Students.DoesNotExist:
        raise Http404("Student not found")
    student_class_id = student.student_class.id
    payment_count = Payment.objects.filter(payment_student__id=student_id).count()
    assignment_count = Assignment.objects.filter(assignment_class__id=student_class_id, assignment_sta=True).count()

    general_notifications_count = General_notification.objects.filter(g_not_audience='General').count()
    student_notifications_count = General_notification.objects.filter(g_not_audience='Students').count()

    class_notifications_count = Notifications.objects.filter(notification_class=student_class_id).count()

    general_notifications = General_notification.objects.filter(g_not_audience='General')
    student_notifications = General_notification.objects.filter(g_not_audience='Students')
    class_notifications = Notifications.objects.filter(notification_class=student_class_id)

    total_notifications_count = general_notifications_count + student_notifications_count + class_notifications_count

    return {
        "payment": payment_count,
        "assignment": assignment_count,
        "get_generals": general_notifications_count,
        "get_general_infos": general_notifications,
        "get_general_ts": student_notifications_count,
        "get_general_info_ts": student_notifications,
        "numbtts": total_notifications_count,
        "get_class_ts": class_notifications_count,
        "get_class_infos": class_notifications
    }
