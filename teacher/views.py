from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from administrator.models import Section, Class, Teacher, Subject, Assign, Assign_subject, Students, Parent, Assign_section, Notifications, Assignment, Assignment_submission, Exam_questions, Term, Session, Grade
from django.contrib.auth.hashers import check_password 
from django.utils.timezone import now
from django.utils.html import escape
from django.urls import reverse
from django.db.models import Q
from django.db.models import Prefetch
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Count
from .forms import ProfilePictureFormT
from django.db.models import Sum,Avg
import json
import pandas as pd
import html
import uuid
import os 

def home(request):
    return render(request, 'teacher/index.html') 

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin_user = Teacher.objects.get(teacher_email=email) 
            if check_password(password, admin_user.teacher_password):
                request.session["teacher_id"] = admin_user.id 
                request.session["teacher_email"] = admin_user.teacher_email  
                request.session["teacher_name"] = admin_user.teacher_fname 
                request.session["teacher_fullname"] = admin_user.teacher_fname + ' ' + admin_user.teacher_othernames
                return redirect('teacher:home') 
            else:
                messages.error(request, "Incorrect password")
        except Teacher.DoesNotExist:
            messages.error(request, "Incorrect email")

    return render(request, "teacher/login.html")  

def logout(request):
    request.session.flush()
    return redirect('teacher:login')

def my_classes(request,id):
    class_list = Assign_subject.objects.select_related("assign_teacher","assign_subject__subject_class").filter(assign_teacher__id=id)
    context = {
    "class_list": class_list,

    }
    return render(request, 'teacher/my_classes.html', context)

def view_mystudents(request,id,sid):
    c_info = get_object_or_404(Class,id=id)
    s_info = get_object_or_404(Subject,id=sid)
    student_list = Students.objects.select_related("student_class").filter(student_class__id=id)
    context = {
    "student_list": student_list,
    "c_info": c_info,
    "s_info": s_info,

    }
    return render(request, 'teacher/my_students.html', context)

def notifications(request,id,sid):
    c_info = get_object_or_404(Class,id=id)
    s_info = get_object_or_404(Subject,id=sid)
    not_list = Notifications.objects.select_related("notification_class").filter(notification_class__id=id,notification_subject=sid)

    context = {
    "c_info": c_info,
    "not_list": not_list,
    "s_info": s_info,

    }
    return render(request, 'teacher/notifications.html', context)

def add_notification(request, id, sid):
    not_info = get_object_or_404(Class, id=id)
    s_info = get_object_or_404(Subject,id=sid)
    if request.method == "POST":
        notification_content = escape(request.POST['notification_content'])
        notification_class = not_info
        notification_subject = s_info

        insert_not = Notifications(
            notification_content=notification_content,
            notification_class=notification_class,
            notification_subject=notification_subject
            )
        insert_not.save()
        messages.success(request, "Notification Added Successfully!")   

    return render(request, "teacher/add_notification.html", {
        "not_info": not_info,
        "s_info": s_info,
        })

def delete_notification(request,id):
    notification_delete_details = get_object_or_404(Notifications, id=id)
    r_id = notification_delete_details.notification_class.id
    sid = notification_delete_details.notification_subject.id
    notification_delete_details.delete()
    return redirect('teacher:notifications', r_id, sid)

def edit_notification(request,id,sid):
    get_not_edit = get_object_or_404(Notifications, id=id)
    get_not_sub = get_object_or_404(Subject, id=sid)
    if request.method == "POST":
        notification_content = escape(request.POST["notification_content"])
        get_not_edit.notification_content = notification_content
        get_not_edit.save()
        messages.success(request, "Notification updated successfully!")
        return redirect("teacher:edit_notification", id, sid)

    return render(request, "teacher/edit_notification.html", {"not": get_not_edit, "get_not_sub": get_not_sub,})

def assignments(request,id,sid):
    get_not_edit = get_object_or_404(Class, id=id)
    get_not_sub = get_object_or_404(Subject, id=sid)
    get_assignment = Assignment.objects.select_related("assignment_class", "assignment_subject").filter(assignment_class=id, assignment_subject=sid)

    return render(request, "teacher/assignments.html", {"not": get_not_edit, "get_not_sub": get_not_sub,"get_assignment": get_assignment,})

def add_assignment(request, id, sid):
    not_info = get_object_or_404(Class, id=id)
    s_info = get_object_or_404(Subject,id=sid)
    if request.method == "POST":
        assignment_deadline = escape(request.POST['assignment_deadline'])
        assignment_instruction = escape(request.POST['assignment_instruction'])
        assignment_material = request.FILES.get('assignment_material')
        assignment_class = not_info
        assignment_subject = s_info
        assignment_check = Assignment.objects.filter(assignment_material=assignment_material)
        if assignment_check.exists():
            messages.error(request, "Assignment File Already exist!")
        else:
            Assignment.objects.create(
                assignment_deadline = assignment_deadline,
                assignment_date = now().date(),
                assignment_instruction = assignment_instruction,
                assignment_material = assignment_material,
                assignment_class = assignment_class,
                assignment_subject = assignment_subject
                )
            messages.success(request, "Assignment Added Successfully!")
    
    return render(request, "teacher/add_assignment.html", {
        "not_info": not_info,
        "s_info": s_info,
        })

def delete_assignment(request,id):
    assignment_delete_details = get_object_or_404(Assignment, id=id)
    r_id = assignment_delete_details.assignment_class.id
    sid = assignment_delete_details.assignment_subject.id
    assignment_delete_details.delete()
    return redirect('teacher:assignments', r_id, sid)

def edit_assignment(request,id):
    assignment_edit_details = get_object_or_404(Assignment, id=id)
    r_id = assignment_edit_details.assignment_class.id
    sid = assignment_edit_details.assignment_subject.id
    if request.method == "POST":
        assignment_deadline = escape(request.POST['assignment_deadline'])
        assignment_instruction = escape(request.POST['assignment_instruction'])
        assignment_edit_details.assignment_instruction = assignment_instruction
        assignment_edit_details.assignment_deadline = assignment_deadline
        assignment_edit_details.save()
        messages.success(request, "Assignment updated successfully!")
        return redirect("teacher:edit_assignment",assignment_edit_details.id )

    return render(request, "teacher/edit_assignment.html", {"not": assignment_edit_details,})

def assignment_status(request,id,ssid):
    assignment_update_details = get_object_or_404(Assignment, id=id)
    r_id = assignment_update_details.assignment_class.id
    sid = assignment_update_details.assignment_subject.id
    if ssid == 1:
        assignment_update_details.assignment_sta = True
    else:
        assignment_update_details.assignment_sta = False
    assignment_update_details.save()
    return redirect('teacher:assignments', r_id, sid)

def assignment_submission(request,id):
    assignment_submit_details = get_object_or_404(Assignment, id=id)
    assignment_answer = Assignment_submission.objects.select_related("submission_student", "submission_assignment").filter(submission_assignment__id=id)

    return render(request, "teacher/assignment_submission.html", {"assignment": assignment_submit_details,"a_answer": assignment_answer, })

def exam_questions(request,id):
    class_list = Assign_subject.objects.select_related("assign_teacher","assign_subject__subject_class").filter(assign_teacher__id=id)
    context = {
    "class_list": class_list,

    }
    return render(request, 'teacher/exam_questions.html', context)

def submitted_questions(request,id,sid):
    get_not_edit = get_object_or_404(Class, id=id)
    get_not_sub = get_object_or_404(Subject, id=sid)
    get_questions = Exam_questions.objects.select_related("question_class", "question_subject").filter(question_class=id, question_subject=sid)

    return render(request, "teacher/submitted_questions.html", {"not": get_not_edit, "get_not_sub": get_not_sub,"get_questions": get_questions,})

def add_exam_question(request, id, sid):
    not_info = get_object_or_404(Class, id=id)
    s_info = get_object_or_404(Subject,id=sid)
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    aid = request.session.get('teacher_id')
    teacher = get_object_or_404(Teacher,id=aid)

    if request.method == "POST":
        question_session = escape(request.POST['question_session'])
        question_term= escape(request.POST['question_term'])
        question_material = request.FILES.get('question_material')
        question_class = not_info
        question_subject = s_info
        question_teacher = teacher
        question_check = Exam_questions.objects.filter(question_material=question_material)
        if question_check.exists():
            messages.error(request, "Question Document File Already exist!")
        else:
            Exam_questions.objects.create(
                question_session = question_session,
                question_submission_date = now().date(),
                question_term = question_term,
                question_material = question_material,
                question_class = question_class,
                question_subject = question_subject,
                question_teacher = question_teacher
                )
            messages.success(request, "Question Document File Uploaded Successfully!")

    
    return render(request, "teacher/add_exam_question.html", {
        "not_info": not_info,
        "s_info": s_info,
        "term_info": term_info,
        "session_info": session_info,
        })

def delete_question(request,id):
    question_delete_details = get_object_or_404(Exam_questions, id=id)
    r_id = question_delete_details.question_class.id
    sid = question_delete_details.question_subject.id
    question_delete_details.delete()
    return redirect('teacher:submitted_questions', r_id, sid)

def score_sheet(request,id):
    class_list = Assign_subject.objects.select_related("assign_teacher","assign_subject__subject_class").filter(assign_teacher__id=id)
    context = {
    "class_list": class_list,

    }
    return render(request, 'teacher/score_sheet.html', context)

def add_grade(request, id, sid):
    get_class = get_object_or_404(Class, id=id)
    get_subject = get_object_or_404(Subject, id=sid)
    students = Students.objects.filter(student_class=id)

    student_data = []
    for student in students:
        grade = Grade.objects.filter(
            grade_class=get_class,
            grade_subject=get_subject,
            grade_student=student
        ).first()  # None if not found

        student_data.append({
            'student': student,
            'grade': grade
        })

    return render(request, "teacher/add_grade.html", {
        "not": get_class,
        "get_not_sub": get_subject,
        "student_data": student_data,
    })

@csrf_exempt
def submit_score(request, student_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            ca = float(data.get('ca_score', 0))
            exam = float(data.get('exam_score', 0))
            total = float(data.get('total_score', 0))
            subject_id = data.get('subject_id')

            if not subject_id:
                return JsonResponse({'status': 'error', 'message': 'Subject ID missing'}, status=400)

            student = get_object_or_404(Students, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            class_obj = student.student_class

            current_term = get_object_or_404(Term, term_sta=True)
            current_session = get_object_or_404(Session, id=1)

            grade, created = Grade.objects.get_or_create(
                grade_student=student,
                grade_class=class_obj,
                grade_subject=subject,
                grade_term=current_term,
                grade_session=current_session,
                defaults={
                    'grade_ca': ca,
                    'grade_exam': exam,
                    'grade_total': total,
                }
            )

            if not created:
                grade.grade_ca = ca
                grade.grade_exam = exam
                grade.grade_total = total
                grade.grade_submission_date = now()
                grade.save()

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def m_class_students(request,id):
    class_info = get_object_or_404(Class, id=id)
    student_info = Students.objects.select_related('student_class').filter(student_class__id=id)
    context = {
    "class_info": class_info,
    "student_info": student_info,
    }
    return render(request, 'teacher/m_class_students.html', context)

def student_record(request,id):
    student_info = get_object_or_404(
    Students.objects.select_related("student_class", "student_parent"), id=id
    )
    
    context = {
    "student_info": student_info,
    }
    return render(request, "teacher/student_record.html", context)

def profile(request,id):
    teacher_info = Teacher.objects.select_related('teacher_section').get(id=id)
    
    context = {
    "teacher_info": teacher_info,
    }
    return render(request, "teacher/profile.html", context)

def change_profile_picture(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        form = ProfilePictureFormT(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            uploaded_file = request.FILES.get("teacher_picture")
            if uploaded_file:
                unique_id = f"{now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
                file_extension = os.path.splitext(uploaded_file.name)[-1] 
                new_filename = f"{unique_id}{file_extension}"

                teacher.teacher_picture.save(f"{new_filename}", uploaded_file)

            form.save()
            messages.success(request, "Profile Picture Updated!")
        else:
            messages.error(request, "Profile Picture Not Updated!")

    else:
        form = ProfilePictureFormT(instance=teacher)

    return render(request, "teacher/change_profile_picture.html", {"form": form, "teacher": teacher})

def edit_profile(request,id):
    get_teacher_edit = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        teacher_fname = escape(request.POST['teacher_fname'])
        teacher_othernames = escape(request.POST['teacher_othernames'])
        teacher_email = escape(request.POST['teacher_email'])
        teacher_phone = escape(request.POST['teacher_phone'])
        teacher_gender = escape(request.POST['teacher_gender'])
        teacher_address = escape(request.POST['teacher_address'])
        teacher_dob = escape(request.POST['teacher_dob'])
        if Teacher.objects.filter(Q(teacher_email=teacher_email) & Q(teacher_section=get_teacher_edit.teacher_section)).exclude(id=id).exists():
            messages.error(request, "Teacher With Thesame Email Already Exist!")
            return redirect(reverse("administrator:edit_teacher", args=[id]))
        else:
            get_teacher_edit.teacher_fname = teacher_fname
            get_teacher_edit.teacher_othernames= teacher_othernames
            get_teacher_edit.teacher_email= teacher_email
            get_teacher_edit.teacher_phone= teacher_phone
            get_teacher_edit.teacher_address= teacher_address
            get_teacher_edit.teacher_dob= teacher_dob
            get_teacher_edit.teacher_gender= teacher_gender
            get_teacher_edit.save()
            messages.success(request, "Profile updated successfully!")
            return redirect(reverse("teacher:edit_profile", args=[id]))

    return render(request, "teacher/edit_profile.html", {"teacher": get_teacher_edit})

def change_password(request,id):
    pass_info = get_object_or_404(Teacher,id=id)
    if request.method == "POST":
        teacher_password = escape(request.POST['teacher_password'])
        cteacher_password = escape(request.POST['cteacher_password'])
        if teacher_password != cteacher_password:
            messages.error(request, "The Two Passwords Did Not Match!")
            return redirect(reverse("teacher:change_password", args=[id]))
        else:
            pass_info.teacher_password = teacher_password
            pass_info.save()
            messages.success(request, "Password updated successfully!")
            return redirect(reverse("teacher:change_password", args=[id]))
    
    return render(request, "teacher/change_password.html")

def compiled_result(request,id):
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    gt = term_info.term_name
    gs = session_info.session_name

    result_info = Grade.objects.select_related("grade_student").filter(
                    grade_class_id=id,
                    grade_term=gt,
                    grade_session=gs
                ).values('grade_student__id','grade_student__student_adm','grade_student__student_fname','grade_student__student_othernames','grade_sta','grade_term','grade_session').annotate(total=Count('id'))
    
    context = {
    "result_info": result_info,
    }
    return render(request, "teacher/compiled_result.html", context)

def print_result(request,id):
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    student_info = get_object_or_404(Students,id=id)
    gt = term_info.term_name
    gs = session_info.session_name
    class_count = Students.objects.filter(student_class=student_info.student_class.id).count()
    result_count = Grade.objects.select_related("grade_student").filter(
                    grade_student_id=id,grade_term=gt, grade_session=gs).count()
    result_info = Grade.objects.select_related("grade_student").filter(
                    grade_student_id=id,grade_term=gt, grade_session=gs)
    total_score = Grade.objects.filter(
    grade_student_id=id,
    grade_term=gt,
    grade_session=gs
    ).aggregate(total_score=Sum('grade_total'))
    student_averages = Grade.objects.filter(
    grade_term=gt,
    grade_session=gs
    ).values('grade_student').annotate(
        avg_score=Avg('grade_total')
    )
    highest_avg = student_averages.order_by('-avg_score').first()
    lowest_avg = student_averages.order_by('avg_score').first()

    average = float(total_score['total_score'])/int(result_count)
    
    context = {
    "result_info": result_info,
    "student_info": student_info,
    "session_info": session_info,
    "term_info": term_info,
    "result_count": result_count,
    "result_count": result_count,
    "total_score": total_score,
    "average": average,
    "highest_avg": highest_avg,
    "lowest_avg": lowest_avg,
    "class_count": class_count,
    }
    return render(request, "teacher/print_result.html", context)