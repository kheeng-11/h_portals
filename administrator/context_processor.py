from .models import Section, Assign, Exam_questions, Term, Session, Events, Blog, Students, Teacher,Grade
from django.shortcuts import get_object_or_404
from django.db.models import Count

def sidebar_data(request):
    sections = Section.objects.all()
    get_questions_count = Exam_questions.objects.filter(question_sta=False).count()
    return {"sections": sections, "get_questions_count": get_questions_count}

def event_data(request):
    get_term_c = get_object_or_404(Term,term_sta=True)
    get_session_c = get_object_or_404(Session,id=1)
    etc = get_term_c.term_name
    esc = get_session_c.session_name
    event_info_c = Events.objects.all().filter(event_term=etc, event_session=esc)

    return {"event_info_c": event_info_c,"get_term_c": get_term_c,"get_session_c": get_session_c,}

def dashboard_data(request):
    get_student_admin = Students.objects.count()
    get_teacher_admin = Teacher.objects.count()
    get_event_admin = Events.objects.count()
    get_blog_admin = Blog.objects.count()
    
    return {"get_student_admin": get_student_admin,"get_teacher_admin": get_teacher_admin,"get_event_admin": get_event_admin,"get_blog_admin": get_blog_admin,}