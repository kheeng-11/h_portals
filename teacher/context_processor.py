from administrator.models import Assign_subject, Exam_questions, Assign, General_notification, Teacher
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404

def dashboard_data(request):
    teacher_id = request.session.get("teacher_id")
    
    if not teacher_id:
        return {
            "get_subjects": 0,
            "get_assignment": 0,
            "myclass": [],
            "get_general": 0,
            "get_general_info": [],
            "get_general_t": 0,
            "get_general_info_t": [],
            "numbtt": 0
        }
    
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        raise Http404("Teacher not found")
    
    subject_count = Assign_subject.objects.filter(assign_teacher__id=teacher_id).count()
    
    assignment_count = Exam_questions.objects.filter(question_sta=False, question_teacher__id=teacher_id).count()
    
    teacher_classes = Assign.objects.filter(assign_teacher=teacher_id)
    
    general_notifications_count = General_notification.objects.filter(g_not_audience='General').count()
    teacher_notifications_count = General_notification.objects.filter(g_not_audience='Teachers').count()
    
    general_notifications = General_notification.objects.filter(g_not_audience='General')
    teacher_notifications = General_notification.objects.filter(g_not_audience='Teachers')
    
    total_notifications_count = general_notifications_count + teacher_notifications_count
    
    return {
        "get_subjects": subject_count,
        "get_assignment": assignment_count,
        "myclass": teacher_classes,
        "get_general": general_notifications_count,
        "get_general_info": general_notifications,
        "get_general_t": teacher_notifications_count,
        "get_general_info_t": teacher_notifications,
        "numbtt": total_notifications_count
    }