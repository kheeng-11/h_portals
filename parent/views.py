from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from administrator.models import Section, Class, Teacher, Subject, Assign, Assign_subject, Students, Parent, Assign_section, Notifications, Assignment, Assignment_submission, Exam_questions, Term, Session, Grade, Payment
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
    return render(request, 'parent/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin_user = Parent.objects.get(parent_email=email) 
            if check_password(password, admin_user.parent_password):
                request.session["parent_id"] = admin_user.id 
                request.session["parent_email"] = admin_user.parent_email 
                request.session["parent_name"] = admin_user.parent_name 
                request.session["parent_fullname"] = admin_user.parent_name
                return redirect('parent:home') 
            else:
                messages.error(request, "Incorrect password")
        except Teacher.DoesNotExist:
            messages.error(request, "Incorrect Admission Number")

    return render(request, "parent/login.html")  

def logout(request):
    request.session.flush()
    return redirect('parent:login')

def profile(request,id):
    parent_info = Parent.objects.get(id=id)
    
    context = {
    "parent_info": parent_info,
    }
    return render(request, "parent/profile.html", context)

def change_profile_picture(request, id):
    parent = get_object_or_404(Parent, id=id)

    if request.method == "POST":
        form = ProfilePictureFormT(request.POST, request.FILES, instance=parent)
        if form.is_valid():
            uploaded_file = request.FILES.get("parent_picture")
            if uploaded_file:
                unique_id = f"{now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
                file_extension = os.path.splitext(uploaded_file.name)[-1] 
                new_filename = f"{unique_id}{file_extension}"

                parent.parent_picture.save(f"{new_filename}", uploaded_file)

            form.save()
            messages.success(request, "Profile Picture Updated!")
        else:
            messages.error(request, "Profile Picture Not Updated!")

    else:
        form = ProfilePictureFormT(instance=parent)

    return render(request, "parent/change_profile_picture.html", {"form": form, "parent": parent})

def edit_profile(request,id):
    get_parent_edit = get_object_or_404(Parent, id=id)
    if request.method == "POST":
        parent_name = escape(request.POST['parent_name'])
        parent_email = escape(request.POST['parent_email'])
        parent_phone = escape(request.POST['parent_phone'])
        parent_address = escape(request.POST['parent_address'])
        if Parent.objects.filter(parent_email=parent_email).exclude(id=id).exists():
            messages.error(request, "Parent With Thesame Email Already Exist!")
            return redirect(reverse("parent:edit_profile", args=[id]))
        else:
            get_parent_edit.parent_name = parent_name
            get_parent_edit.parent_email= parent_email
            get_parent_edit.parent_phone= parent_phone
            get_parent_edit.parent_address= parent_address
            get_parent_edit.save()
            messages.success(request, "Profilr updated successfully!")
            return redirect(reverse("parent:edit_profile", args=[id]))

    return render(request, "parent/edit_profile.html", {"parent": get_parent_edit})

def change_password(request,id):
    pass_info = get_object_or_404(Parent,id=id)
    if request.method == "POST":
        parent_password = escape(request.POST['parent_password'])
        cparent_password = escape(request.POST['cparent_password'])
        if parent_password != cparent_password:
            messages.error(request, "The Two Passwords Did Not Match!")
            return redirect(reverse("parent:change_password", args=[id]))
        else:
            pass_info.parent_password = parent_password
            pass_info.save()
            messages.success(request, "Password updated successfully!")
            return redirect(reverse("parent:change_password", args=[id]))
    
    return render(request, "parent/change_password.html")

def my_children(request,id):
    student_info_ = Students.objects.select_related('student_class', 'student_class__class_section').filter(student_parent__id=id)
    context = {
    "student_info_": student_info_,
    }
    return render(request, 'parent/my_children.html', context)

def payment_record(request,id):
    student_info_ = Students.objects.select_related('student_class', 'student_class__class_section').filter(student_parent__id=id)
    context = {
    "student_info_": student_info_,
    }
    return render(request, 'parent/payment_record.html', context)

def student_payment_record(request,id):
    student = get_object_or_404(Students,id=id)
    student_info = Payment.objects.select_related('payment_student').filter(payment_student__id = id)
    context = {
    "student_info": student_info,
    "student": student,
    }
    return render(request, 'parent/student_payment_record.html', context)

def student_payment_reciept(request,id):
    student_info = Payment.objects.select_related('payment_student').filter(id = id)
    context = {
    "student_info": student_info,
    }
    return render(request, 'parent/student_payment_reciept.html', context)

def compiled_result(request,id):
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    gt = term_info.term_name
    gs = session_info.session_name

    result_info = Grade.objects.select_related("grade_student").filter(
                    grade_student__student_parent=id,
                    grade_term=gt,
                    grade_session=gs
                ).values('grade_student__id','grade_student__student_adm','grade_student__student_fname','grade_student__student_othernames','grade_sta','grade_term','grade_session').annotate(total=Count('id'))
    context = {
    "result_info": result_info,
    }
    return render(request, 'parent/compiled_result.html', context)

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