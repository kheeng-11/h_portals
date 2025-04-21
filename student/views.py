from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from administrator.models import Section, Class, Teacher, Subject, Assign, Assign_subject, Students, Parent, Assign_section, Notifications, Assignment, Assignment_submission, Exam_questions, Term, Session, Grade, Payment, Assignment_submission
from django.contrib.auth.hashers import check_password 
from django.utils.timezone import now
from django.utils.html import escape
from django.urls import reverse
from django.db.models import Q
from django.db.models import Prefetch
from django.http import JsonResponse
from .forms import ProfilePictureFormT
from django.db.models import Count
from django.db.models import Sum,Avg
import json
import pandas as pd
import html
import uuid
import os 

def home(request):
    return render(request, 'student/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST['adm_no']
        password = request.POST['password']

        try:
            admin_user = Students.objects.get(student_adm=email) 
            if check_password(password, admin_user.student_password):
                request.session["student_id"] = admin_user.id 
                request.session["student_admission"] = admin_user.student_adm 
                request.session["student_name"] = admin_user.student_fname 
                request.session["student_fullname"] = admin_user.student_fname + ' ' + admin_user.student_othernames
                return redirect('student:home') 
            else:
                messages.error(request, "Incorrect password")
        except Teacher.DoesNotExist:
            messages.error(request, "Incorrect Admission Number")

    return render(request, "student/login.html")  

def logout(request):
    request.session.flush()
    return redirect('student:login')

def profile(request,id):
    student_info = get_object_or_404(
    Students.objects.select_related("student_class", "student_parent"), id=id
    )
    
    context = {
    "student_info": student_info,
    }
    return render(request, "student/profile.html", context)

def change_profile_picture(request, id):
    student = get_object_or_404(Students, id=id)

    if request.method == "POST":
        form = ProfilePictureFormT(request.POST, request.FILES, instance=student)
        if form.is_valid():
            uploaded_file = request.FILES.get("student_picture")
            if uploaded_file:
                unique_id = f"{now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
                file_extension = os.path.splitext(uploaded_file.name)[-1] 
                new_filename = f"{unique_id}{file_extension}"

                student.student_picture.save(f"{new_filename}", uploaded_file)

            form.save()
            messages.success(request, "Profile Picture Updated!")
        else:
            messages.error(request, "Profile Picture Not Updated!")

    else:
        form = ProfilePictureFormT(instance=student)

    return render(request, "student/change_profile_picture.html", {"form": form, "student": student})

def edit_profile(request,id):
    get_student_edit = get_object_or_404(Students, id=id)
    if request.method == "POST":
        student_address = escape(request.POST['student_address'])
        student_dob = escape(request.POST['student_dob'])
        student_gender= escape(request.POST['student_gender'])

        get_student_edit.student_address= student_address
        get_student_edit.student_dob= student_dob
        get_student_edit.student_gender= student_gender
        get_student_edit.save()
        messages.success(request, " updated successfully!")
        return redirect(reverse("student:edit_profile", args=[id]))

    return render(request, "student/edit_profile.html", {"student": get_student_edit})

def change_password(request,id):
    pass_info = get_object_or_404(Students,id=id)
    if request.method == "POST":
        student_password = escape(request.POST['student_password'])
        cstudent_password = escape(request.POST['cstudent_password'])
        if student_password != cstudent_password:
            messages.error(request, "The Two Passwords Did Not Match!")
            return redirect(reverse("student:change_password", args=[id]))
        else:
            pass_info.student_password = student_password
            pass_info.save()
            messages.success(request, "Password updated successfully!")
            return redirect(reverse("student:change_password", args=[id]))
    
    return render(request, "student/change_password.html")

def my_record(request,id):
    student = get_object_or_404(Students,id=id)
    student_info = Payment.objects.select_related('payment_student').filter(payment_student__id = id)
    context = {
    "student_info": student_info,
    "student": student,
    }
    return render(request, 'student/my_record.html', context)

def payment_reciept(request,id):
    student_info = Payment.objects.select_related('payment_student').filter(id = id)
    context = {
    "student_info": student_info,
    }
    return render(request, 'student/payment_reciept.html', context)

def assignments(request,id):
    st = get_object_or_404(Students, id = id)
    cl= st.student_class.id
    assignment = Assignment.objects.select_related("assignment_class").filter(assignment_class__id=cl)
    context = {
    "assignment": assignment,
    }
    return render(request, 'student/assignments.html', context)

def submissions(request,id):
    sa= get_object_or_404(Assignment,id=id)
    sid = request.session.get('student_id')
    st = Assignment_submission.objects.select_related("submission_assignment","submission_student",).filter(Q(submission_assignment = id) & Q(submission_student = sid))
    context = {
    "st": st,
    "sa": sa,
    }
    return render(request, 'student/submissions.html', context)

def submit_assignment(request, id):
    sa= get_object_or_404(Assignment,id=id)
    sid = request.session.get('student_id')
    sids= get_object_or_404(Students,id=sid)
    if request.method == "POST":
        submission_comment = escape(request.POST['submission_comment'])
        submission_material = request.FILES.get('submission_material')
        submission_student = sids
        submission_assignment = sa
        assignment_check = Assignment_submission.objects.filter(submission_student=submission_student,submission_assignment=submission_assignment )
        if assignment_check.exists():
            messages.error(request, "You have already Submitted!")
        else:
            Assignment_submission.objects.create(
                submission_comment = submission_comment,
                submission_date = now().date(),
                submission_student = submission_student,
                submission_material = submission_material,
                submission_assignment = submission_assignment
                )
            messages.success(request, "Assignment Submitted Successfully!")
    
    return render(request, "student/submit_assignment.html", {
        "sa": sa,
        })

def delete_submission(request,id):
    s_info = get_object_or_404(Assignment_submission, id=id)
    asi= s_info.submission_assignment.id
    s_info.delete()

    return redirect('student:submissions', asi)

def compiled_result(request,id):
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    gt = term_info.term_name
    gs = session_info.session_name

    result_info = Grade.objects.select_related("grade_student").filter(
                    grade_student_id=id,
                    grade_term=gt,
                    grade_session=gs
                ).values('grade_student__id','grade_student__student_adm','grade_student__student_fname','grade_student__student_othernames','grade_sta','grade_term','grade_session').annotate(total=Count('id'))
    
    context = {
    "result_info": result_info,
    }
    return render(request, "student/compiled_result.html", context)

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
    return render(request, "student/print_result.html", context)