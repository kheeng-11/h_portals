from .models import Section, Assign, Exam_questions, Term, Session, Events, Blog, Students, Teacher,Grade
from django.shortcuts import get_object_or_404
from django.db.models import Count

def index_date(request):
    sections = Section.objects.all()
    get_questions_count = Exam_questions.objects.filter(question_sta=False).count()
    return {"sections": sections, "get_questions_count": get_questions_count}

