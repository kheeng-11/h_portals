from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, Section, Class, Teacher, Subject, Assign, Assign_subject, Students, Parent, Assign_section, Exam_questions, Payment, Term, Session, Events, General_notification, Blog, Gallery, Grade
from django.contrib import messages
from django.contrib.auth.hashers import check_password 
from django.utils.timezone import now
from django.utils.html import escape
from django.urls import reverse
from django.db.models import Q
from django.db.models import Prefetch
import pandas as pd
from django.db.models import Count
from .forms import ExcelUploadForm, ProfilePictureForm, ProfilePictureFormT, ProfilePictureFormP
import html
import uuid
import os

def home(request):
    return render(request, 'administrator/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin_user = Admin.objects.get(admin_usermail=email) 
            if check_password(password, admin_user.admin_password):
                request.session["admin_id"] = admin_user.id 
                request.session["admin_email"] = admin_user.admin_usermail  
                request.session["admin_name"] = admin_user.admin_fname 
                request.session["admin_fullname"] = admin_user.admin_fname + ' ' + admin_user.admin_othernames
                return redirect('administrator:home') 
            else:
                messages.error(request, "Incorrect password")
        except Admin.DoesNotExist:
            messages.error(request, "Incorrect email")

    return render(request, "administrator/login.html")  

def logout(request):
    request.session.flush()
    return redirect('administrator:login')


def manage_sections(request):
    section_list = Section.objects.all()
    return render(request, 'administrator/manage_sections.html',{"sections": section_list})

def add_section(request):
    if request.method == "POST":
        section_name = escape(request.POST['section_name'])
        setion_check = Section.objects.filter(section_name=section_name)
        if setion_check.exists():
            messages.error(request, "Section Name Already exist!")
        else:
            insert_section  = Section(
                section_name = section_name,
                section_added_on = now().date(),
                )
            insert_section.save()
            messages.success(request, "Section Added Successfully!")
            
    return render(request, 'administrator/add_section.html')

def delete_section(request,id):
    section_detail = get_object_or_404(Section, id=id)
    section_detail.delete()
    return redirect('administrator:manage_sections')

def edit_section(request,id):
    get_section_edit = get_object_or_404(Section, id=id)
    if request.method == "POST":
        section_name = escape(request.POST["section_name"])
        if Section.objects.filter(section_name=section_name).exclude(id=id).exists():
            messages.error(request, "Section Name Already exist!")
            return redirect(reverse("administrator:edit_section", args=[id]))
        else:
            get_section_edit.section_name = section_name
            get_section_edit.save()
            messages.success(request, "Section details updated successfully!")
            return redirect(reverse("administrator:edit_section", args=[id]))

    return render(request, "administrator/edit_section.html", {"section": get_section_edit})

def section_info(request, id):
    section_info = Section.objects.filter(id=id)
    section_classes = Class.objects.filter(class_section__id=id).prefetch_related(
        Prefetch("assign_set", queryset=Assign.objects.select_related("assign_teacher"))
    )
    section_teacher_info = Teacher.objects.select_related("teacher_section").filter(teacher_section__id=id)
    secthead = Assign_section.objects.select_related("assign_steacher","assign_section").filter(assign_section__id=id)
    context = {
        "section_info": section_info,
        "section_class_info": section_classes,
        "section_teacher_info": section_teacher_info,
        "secthead": secthead,
    }
    return render(request, "administrator/section_info.html", context)

def add_class(request, id):
    section_info = get_object_or_404(Section, id=id)

    if request.method == "POST":
        class_name = escape(request.POST['class_name'])
        class_section = section_info 
        class_check = Class.objects.filter(
            class_name=class_name, class_section=class_section
        )
        if class_check.exists():
            messages.error(request, "Class Name Already Exists!")
        else:
            insert_class = Class(class_name=class_name, class_section=class_section)
            insert_class.save()
            messages.success(request, "Class Added Successfully!")

    return render(request, "administrator/add_class.html", {"section_info": section_info})

def delete_class(request,id):
    class_delete_details = get_object_or_404(Class, id=id)
    r_id = class_delete_details.class_section.id
    class_delete_details.delete()
    return redirect('administrator:section_info', r_id)

def edit_class(request,id):
    get_class_edit = get_object_or_404(Class, id=id)
    if request.method == "POST":
        class_name = escape(request.POST["class_name"])
        if Class.objects.filter(class_name=class_name).exclude(id=id).exists():
            messages.error(request, "Class Name Already exist!")
            return redirect(reverse("administrator:edit_class", args=[id]))
        else:
            get_class_edit.class_name = class_name
            get_class_edit.save()
            messages.success(request, "Class details updated successfully!")
            return redirect(reverse("administrator:edit_class", args=[id]))

    return render(request, "administrator/edit_class.html", {"class": get_class_edit})

def add_teacher(request, id):
    section_info = get_object_or_404(Section, id=id)

    if request.method == "POST":
        teacher_fname = escape(request.POST['teacher_fname'])
        teacher_othernames = escape(request.POST['teacher_othernames'])
        teacher_email = escape(request.POST['teacher_email'])
        teacher_phone = escape(request.POST['teacher_phone'])
        teacher_password = '1234'
        teacher_section = section_info 
        teacher_check = Teacher.objects.filter(
            Q(teacher_email=teacher_email) & Q(teacher_section=teacher_section)
        )
        if teacher_check.exists():
            messages.error(request, "Teacher With Thesame Email Already Exist!")
        else:
            insert_teacher = Teacher(teacher_fname=teacher_fname, teacher_othernames=teacher_othernames, teacher_email=teacher_email, teacher_phone=teacher_phone, teacher_password=teacher_password, teacher_section=teacher_section)
            insert_teacher.save()
            messages.success(request, "Teacher Added Successfully!")

    return render(request, "administrator/add_teacher.html", {"section_info": section_info})

def edit_teacher(request,id):
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
            messages.success(request, "Teacher details updated successfully!")
            return redirect(reverse("administrator:edit_teacher", args=[id]))

    return render(request, "administrator/edit_teacher.html", {"teacher": get_teacher_edit})

def manage_subjects(request,id):
    class_info = get_object_or_404(Class, id=id)
    subject_list = Subject.objects.filter(subject_class=id).prefetch_related(
        Prefetch("assign_subject_set", queryset=Assign_subject.objects.select_related("assign_teacher"))
    )
    context = {
    "subjects": subject_list,
    "class_info": class_info,

    }
    return render(request, 'administrator/manage_subjects.html', context)

def delete_teacher(request,id):
    teacher_delete_details = get_object_or_404(Teacher, id=id)
    r_id = teacher_delete_details.teacher_section.id
    teacher_delete_details.delete()
    return redirect('administrator:section_info', r_id)

def add_subject(request, id):
    class_info = get_object_or_404(Class, id=id)

    if request.method == "POST":
        subject_name = escape(request.POST['subject_name'])
        subject_class = class_info 
        subject_check = Subject.objects.filter(
            subject_name=subject_name, subject_class=subject_class
        )
        if subject_check.exists():
            messages.error(request, "Subject Name Already Exists!")
        else:
            insert_subject = Subject(subject_name=subject_name, subject_class=subject_class)
            insert_subject.save()
            messages.success(request, "Subject Added Successfully!")

    return render(request, "administrator/add_subject.html", {"class_info": class_info})

def edit_subject(request,id):
    get_subject_edit = get_object_or_404(Subject, id=id)
    if request.method == "POST":
        subject_name = escape(request.POST["subject_name"])
        if Subject.objects.filter(subject_class=get_subject_edit.subject_class, subject_name=subject_name).exclude(id=id).exists():
            messages.error(request, "Subject Name Already exist!")
            return redirect(reverse("administrator:edit_subject", args=[id]))
        else:
            get_subject_edit.subject_name = subject_name
            get_subject_edit.save()
            messages.success(request, "Subject details updated successfully!")
            return redirect(reverse("administrator:edit_subject", args=[id]))

    return render(request, "administrator/edit_subject.html", {"subject": get_subject_edit})

def delete_subject(request,id):
    subject_delete_details = get_object_or_404(Subject, id=id)
    r_id = subject_delete_details.subject_class.id
    subject_delete_details.delete()
    return redirect('administrator:manage_subjects', r_id)

def assign(request, id):
    section_info = get_object_or_404(Section, id=id)
    class_list = Class.objects.select_related("class_section").filter(class_section__id=id)
    teacher_list = Teacher.objects.select_related("teacher_section").filter(teacher_section__id=id)

    context = {
    "section_info": section_info,
    "class_list": class_list,
    "teacher_list": teacher_list,
    }

    if request.method == "POST":
        class_name = escape(request.POST['class_name'])
        teacher_name = escape(request.POST['teacher_name'])
        assign_class = get_object_or_404(Class, id=class_name)
        assign_teacher = get_object_or_404(Teacher, id=teacher_name)
        assign_check = Assign.objects.filter(
            Q(assign_teacher=assign_teacher) & Q(assign_class=assign_class)
        )
        assignc_check = Assign.objects.filter(
            assign_class=assign_class
        )
        if assign_check.exists():
            messages.error(request, "Assignment Already Exists!")
        elif assignc_check.exists():
            messages.error(request, "Class Already have A Class Master!")
        else:
            insert_assignment = Assign(assign_class=assign_class, assign_teacher=assign_teacher)
            insert_assignment.save()
            messages.success(request, "Class Master Assigned Successfully!")

    return render(request, "administrator/assign.html", context)

def assign_subject(request, id):
    class_info = get_object_or_404(Class, id=id)
    subject_list = Subject.objects.select_related("subject_class").filter(subject_class__id=id)
    teacher_list = Teacher.objects.select_related("teacher_section").filter(teacher_section__id=class_info.class_section.id)

    context = {
    "subject_list": subject_list,
    "class_info": class_info,
    "teacher_list": teacher_list,
    }
    if request.method == "POST":
        subject_name = escape(request.POST['subject_name'])
        teacher_name = escape(request.POST['teacher_name'])
        assign_subject = get_object_or_404(Subject, id=subject_name)
        assign_teacher = get_object_or_404(Teacher, id=teacher_name)
        assign_check = Assign_subject.objects.filter(
            Q(assign_teacher=assign_teacher) & Q(assign_subject=assign_subject)
        )
        assigns_check = Assign_subject.objects.filter(
            assign_subject=assign_subject
        )
        if assign_check.exists():
            messages.error(request, "Assignment Already Exists!")
        elif assigns_check.exists():
            messages.error(request, "Subject Already Assigned!")
        else:
            insert_assignment = Assign_subject(assign_subject=assign_subject, assign_teacher=assign_teacher)
            insert_assignment.save()
            messages.success(request, "Assignment Made Successfully!")

    return render(request, "administrator/assign_subject.html", context)

def manage_students(request,id):
    class_info = get_object_or_404(Class, id=id)
    student_info = Students.objects.select_related('student_class').filter(student_class__id=id)
    context = {
    "class_info": class_info,
    "student_info": student_info,
    }
    return render(request, 'administrator/manage_students.html', context)

def add_excel(request,id):
    class_info = get_object_or_404(Class, id=id)
    student_pass = '1234student'
    parent_pass = '1234parent'
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]
                df = pd.read_excel(excel_file, engine="openpyxl")

                required_columns = {"First Name", "Other Names", "Admission Number", "Parent Email"}
                if not required_columns.issubset(df.columns):
                    messages.error(request, "Invalid file format. Missing required columns.")
                    return redirect("add_excel")

                for _, row in df.iterrows():
                    if pd.isna(row["First Name"]) or pd.isna(row["Other Names"]) or pd.isna(row["Admission Number"]) or pd.isna(row["Parent Email"]):
                        messages.warning(request, "Skipping row with missing values.")
                        continue

                    if Students.objects.filter(student_adm=row["Admission Number"]).exists():
                        messages.warning(request, f"Skipping duplicate Admission Number: {row['Admission Number']}")
                        continue

                    # Check if parent exists
                    parent, created = Parent.objects.get_or_create(
                        parent_email=row["Parent Email"],
                        defaults={"parent_password": parent_pass}
                    )

                    Students.objects.create(
                        student_fname=row["First Name"],
                        student_othernames=row["Other Names"],
                        student_parent=parent,
                        student_adm=row["Admission Number"],
                        student_password=student_pass,
                        student_class=class_info,
                    )

                messages.success(request, "Student Data Uploaded Successfully!")
                return redirect(reverse("administrator:add_excel", args=[id]))


            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return redirect(reverse("administrator:add_excel", args=[id]))

    else:
        form = ExcelUploadForm()
    context = {
    "class_info": class_info,
    "form": form,

    }
    return render(request, "administrator/add_excel.html", context)

def add_student(request,id):
    class_info = get_object_or_404(Class, id=id)
    student_pass = '1234student'
    parent_pass = '1234parent'
    if request.method == "POST":
        student_fname = escape(request.POST['student_fname'])
        student_adm = escape(request.POST['student_adm'])
        student_othernames = escape(request.POST['student_othernames'])
        parent_email= escape(request.POST['parent_email'])

        if Students.objects.filter(student_adm=student_adm).exists():
            messages.error(request, "Student with Admission number " + student_adm + " Already Exist!")
        else:
            parent, created = Parent.objects.get_or_create(
                parent_email=parent_email,
                defaults={"parent_password": parent_pass}
            )
            Students.objects.create(
                student_fname=student_fname,
                student_othernames=student_othernames,
                student_parent=parent,
                student_adm=student_adm,
                student_password=student_pass,
                student_class=class_info,
            ) 
            messages.success(request, "Student with Admission number " + student_adm + " Created!")

    context = {
    "class_info": class_info,
    }
    return render(request, "administrator/add_student.html", context)

def student_record(request,id):
    student_info = get_object_or_404(
    Students.objects.select_related("student_class", "student_parent"), id=id
    )
    
    context = {
    "student_info": student_info,
    }
    return render(request, "administrator/student_record.html", context)

def change_student_pic(request, id):
    student = get_object_or_404(Students, id=id)

    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=student)
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
        form = ProfilePictureForm(instance=student)

    return render(request, "administrator/change_studentpic.html", {"form": form, "student": student})

def edit_student(request,id):
    get_student_edit = get_object_or_404(Students, id=id)
    if request.method == "POST":
        student_fname = escape(request.POST['student_fname'])
        student_othernames = escape(request.POST['student_othernames'])
        student_address = escape(request.POST['student_address'])
        student_dob = escape(request.POST['student_dob'])
        student_gender= escape(request.POST['student_gender'])

        get_student_edit.student_fname = student_fname
        get_student_edit.student_othernames= student_othernames
        get_student_edit.student_address= student_address
        get_student_edit.student_dob= student_dob
        get_student_edit.student_gender= student_gender
        get_student_edit.save()
        messages.success(request, "Student details updated successfully!")
        return redirect(reverse("administrator:edit_student", args=[id]))

    return render(request, "administrator/edit_student.html", {"student": get_student_edit})

def delete_student(request,id):
    student_delete_details = get_object_or_404(Students, id=id)
    r_id = student_delete_details.student_class.id
    student_delete_details.delete()
    return redirect('administrator:manage_students', r_id)

def students(request):
    student_info_ = Students.objects.select_related('student_class', 'student_class__class_section')
    context = {
    "student_info_": student_info_,
    }
    return render(request, 'administrator/students.html', context)

def teacher_record(request,id):
    teacher_info = Teacher.objects.select_related('teacher_section').get(id=id)
    
    context = {
    "teacher_info": teacher_info,
    }
    return render(request, "administrator/teacher_record.html", context)

def change_teacher_pic(request, id):
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

    return render(request, "administrator/change_teacherpic.html", {"form": form, "teacher": teacher})

def teachers(request):
    teacher_info_ = Teacher.objects.select_related('teacher_section')
    context = {
    "teacher_info_": teacher_info_,
    }
    return render(request, 'administrator/teachers.html', context)

def assign_section(request):
    section_list = Section.objects.all()
    teacher_list = Teacher.objects.all()

    context = {
    "section_list": section_list,
    "teacher_list": teacher_list,
    }
    if request.method == "POST":
        section_name = escape(request.POST['section_name'])
        teacher_name = escape(request.POST['teacher_name'])
        assign_section = get_object_or_404(Section, id=section_name)
        assign_teacher = get_object_or_404(Teacher, id=teacher_name)
        assign_check = Assign_section.objects.filter(
            Q(assign_steacher=assign_teacher) & Q(assign_section=assign_section)
        )
        assignc_check = Assign_section.objects.filter(
            assign_section=assign_section
        )
        if assign_check.exists():
            messages.error(request, "Assignment Already Exists!")
        elif assignc_check.exists():
            messages.error(request, "Section Already have A Sectional Head!")
        else:
            insert_assignment = Assign_section(assign_section=assign_section, assign_steacher=assign_teacher)
            insert_assignment.save()
            messages.success(request, "Sectional Head Assigned Successfully!")


    return render(request, "administrator/assign_section.html", context)

def sectional_head(request):
    section_list_assign = Assign_section.objects.select_related('assign_steacher', 'assign_section')
    context = {
    "section_list_assign": section_list_assign,
    }

    return render(request, "administrator/sectional_head.html", context)

def delete_section_assignment(request,id):
    section_delete_details = get_object_or_404(Assign_section, id=id)
    section_delete_details.delete()
    return redirect('administrator:sectional_head')

def parents(request):
    parent_info_ = Parent.objects.all()
    context = {
    "parent_info_": parent_info_,
    }
    return render(request, 'administrator/parents.html', context)

def parent_record(request,id):
    parent_info = Parent.objects.get(id=id)
    
    context = {
    "parent_info": parent_info,
    }
    return render(request, "administrator/parent_record.html", context)

def change_parent_pic(request, id):
    parent = get_object_or_404(Parent, id=id)

    if request.method == "POST":
        form = ProfilePictureFormP(request.POST, request.FILES, instance=parent)
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
        form = ProfilePictureFormP(instance=parent)

    return render(request, "administrator/change_parentpic.html", {"form": form, "parent": parent})

def edit_parent(request,id):
    get_parent_edit = get_object_or_404(Parent, id=id)
    if request.method == "POST":
        parent_name = escape(request.POST['parent_name'])
        parent_email = escape(request.POST['parent_email'])
        parent_phone = escape(request.POST['parent_phone'])
        parent_address = escape(request.POST['parent_address'])
        if Parent.objects.filter(parent_email=parent_email).exclude(id=id).exists():
            messages.error(request, "Parent With Thesame Email Already Exist!")
            return redirect(reverse("administrator:edit_parent", args=[id]))
        else:
            get_parent_edit.parent_name = parent_name
            get_parent_edit.parent_email= parent_email
            get_parent_edit.parent_phone= parent_phone
            get_parent_edit.parent_address= parent_address
            get_parent_edit.save()
            messages.success(request, "Parent details updated successfully!")
            return redirect(reverse("administrator:edit_parent", args=[id]))

    return render(request, "administrator/edit_parent.html", {"parent": get_parent_edit})

def unapproved_exams(request):
    get_questions = Exam_questions.objects.select_related("question_class", "question_subject", "question_teacher").filter(question_sta=False)

    return render(request, "administrator/unapproved_exams.html", {"get_questions": get_questions,})

def update_exam(request,id):
    exam_info = get_object_or_404(Exam_questions, id=id)

    if request.method == "POST":
        question_sta = escape(request.POST['question_sta'])
        question_approve_comment = escape(request.POST['question_approve_comment'])
        if question_sta == 'False':
            exam_info.delete()
        else:
            exam_info.question_sta = question_sta
            exam_info.question_approve_comment = question_approve_comment
            exam_info.question_approve_date = now().date(),
            exam_info.save()
        messages.success(request, "Exam Question Request Updated Successfully!")

    context = {
    "exam_info": exam_info,
    }
    return render(request, "administrator/update_exam.html", context)

def approved_exams(request):
    get_questions = Exam_questions.objects.select_related("question_class", "question_subject", "question_teacher").filter(question_sta=True)

    return render(request, "administrator/approved_exams.html", {"get_questions": get_questions,})

def record_payment(request):
    student_info_ = Students.objects.select_related('student_class', 'student_class__class_section')
    context = {
    "student_info_": student_info_,
    }
    return render(request, 'administrator/record_payment.html', context)

def update_exam(request,id):
    exam_info = get_object_or_404(Exam_questions, id=id)

    if request.method == "POST":
        question_sta = escape(request.POST['question_sta'])
        question_approve_comment = escape(request.POST['question_approve_comment'])
        if question_sta == 'False':
            exam_info.delete()
        else:
            exam_info.question_sta = question_sta
            exam_info.question_approve_comment = question_approve_comment
            exam_info.question_approve_date = now().date(),
            exam_info.save()
        messages.success(request, "Exam Question Request Updated Successfully!")

    context = {
    "exam_info": exam_info,
    }
    return render(request, "administrator/update_exam.html", context)
    
def add_record(request,id):
    student_info = get_object_or_404(Students, id=id)
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)

    if request.method == "POST":
        payment_term = term_info
        payment_session= session_info
        payment_student = student_info
        payment_description = escape(request.POST['payment_description'])
        payment_amount = escape(request.POST['payment_amount'])

        
        Payment.objects.create(
            payment_term = payment_term,
            payment_date = now().date(),
            payment_session = payment_session,
            payment_student = payment_student,
            payment_description = payment_description,
            payment_amount = payment_amount,
            )
        messages.success(request, "Payment Recorded Successfully!")

    context = {
    "student_info": student_info,
    }
    return render(request, "administrator/add_record.html", context)

def student_payment_record(request,id):
    student = get_object_or_404(Students,id=id)
    student_info = Payment.objects.select_related('payment_student').filter(payment_student__id = id)
    context = {
    "student_info": student_info,
    "student": student,
    }
    return render(request, 'administrator/student_payment_record.html', context)

def student_payment_reciept(request,id):
    student_info = Payment.objects.select_related('payment_student').filter(id = id)
    context = {
    "student_info": student_info,
    }
    return render(request, 'administrator/student_payment_reciept.html', context)

def delete_student_payment(request,id):
    payment_details = get_object_or_404(Payment, id=id)
    r_id = payment_details.payment_student.id
    payment_details.delete()
    return redirect('administrator:student_payment_record', r_id)

def payment_record(request):
    student_info = Payment.objects.select_related('payment_student')
    context = {
    "student_info": student_info,
    }
    return render(request, 'administrator/payment_record.html', context)

def print_all_record(request):
    student_info = Payment.objects.select_related('payment_student')
    context = {
    "student_info": student_info,
    }
    return render(request, 'administrator/print_all_record.html', context)

def school_calendar(request):
    get_term = get_object_or_404(Term,term_sta=True)
    get_session = get_object_or_404(Session,id=1)
    et = get_term.term_name
    es = get_session.session_name
    event_info = Events.objects.all().filter(event_term=et, event_session=es)
    context = {
    "event_info": event_info,
    }
    return render(request, 'administrator/school_calendar.html', context)

def add_event(request):
    get_term = get_object_or_404(Term,term_sta=True)
    get_session = get_object_or_404(Session,id=1)
    et = get_term.term_name
    es = get_session.session_name

    if request.method == "POST":
        event_name = escape(request.POST['event_name'])
        event_date = escape(request.POST['event_date'])
        event_check = Events.objects.filter(
            event_date=event_date
        )
        if event_check.exists():
            messages.error(request, "Event On The Selected Date Already Exist!")
        else:
            insert_event = Events(event_name=event_name, event_date=event_date, event_term=et, event_session=es)
            insert_event.save()
            messages.success(request, "Event Added Successfully!")

    return render(request, "administrator/add_event.html")

def edit_event(request,id):
    get_event_edit = get_object_or_404(Events, id=id)
    if request.method == "POST":
        event_date = escape(request.POST['event_date'])
        event_name = escape(request.POST['event_name'])

        if Events.objects.filter(event_date=event_date).exclude(id=id).exists():
            messages.error(request, "Event On The Selected Date Already Exist!")
            return redirect(reverse("administrator:edit_event", args=[id]))
        else:
            get_event_edit.event_date = event_date
            get_event_edit.event_name= event_name
            get_event_edit.save()
            messages.success(request, "Event details updated successfully!")
            return redirect(reverse("administrator:edit_event", args=[id]))

    return render(request, "administrator/edit_event.html", {"event": get_event_edit})

def delete_event(request,id):
    event_details = get_object_or_404(Events, id=id)
    event_details.delete()
    return redirect('administrator:school_calendar')

def general_notification(request):
    get_term = get_object_or_404(Term,term_sta=True)
    get_session = get_object_or_404(Session,id=1)
    et = get_term.term_name
    es = get_session.session_name
    not_info = General_notification.objects.all().filter(g_not_term=et, g_not_session=es)
    context = {
    "not_info": not_info,
    }
    return render(request, 'administrator/general_notification.html', context)

def add_general_notification(request):
    get_term = get_object_or_404(Term,term_sta=True)
    get_session = get_object_or_404(Session,id=1)
    et = get_term.term_name
    es = get_session.session_name

    if request.method == "POST":
        g_not_audience = escape(request.POST['g_not_audience'])
        g_not_notification = escape(request.POST['g_not_notification'])
        
        insert_not = General_notification(g_not_audience=g_not_audience, g_not_notification=g_not_notification, g_not_term=et, g_not_session=es,g_not_date=now().date())
        insert_not.save()
        messages.success(request, "Notification Added Successfully!")
   
    return render(request, 'administrator/add_general_notification.html')

def edit_general_notification(request,id):
    get_g_n = get_object_or_404(General_notification, id=id)
    if request.method == "POST":
        g_not_audience = escape(request.POST['g_not_audience'])
        g_not_notification = escape(request.POST['g_not_notification'])

        get_g_n.g_not_audience = g_not_audience
        get_g_n.g_not_notification= g_not_notification
        get_g_n.save()
        messages.success(request, "Notification details updated successfully!")

    return render(request, "administrator/edit_general_notification.html", {"not": get_g_n})

def delete_general_notification(request,id):
    gn_details = get_object_or_404(General_notification, id=id)
    gn_details.delete()
    return redirect('administrator:general_notification')

def blogs(request):
    blog_info = Blog.objects.all()
    context = {
    "blog_info": blog_info,
    }
    return render(request, 'administrator/blogs.html', context)

def add_blog(request):
    get_term = get_object_or_404(Term,term_sta=True)
    get_session = get_object_or_404(Session,id=1)
    et = get_term.term_name
    es = get_session.session_name
    if request.method == "POST":
        blog_title = escape(request.POST['blog_title'])
        blog_content = escape(request.POST['blog_content'])
        blog_cover = request.FILES.get('blog_cover')
        blog_date = now().date(),
        blog_check = Blog.objects.filter(
            blog_title=blog_title,blog_term=et,blog_session=es
        )
        if blog_check.exists():
            messages.error(request, "Blog Already Exist!")
        else:
            insert_blog = Blog(blog_title=blog_title, blog_content=blog_content, blog_cover=blog_cover, blog_date=blog_date, blog_term=et, blog_session=es)
            insert_blog.save()
            messages.success(request, "Blog Added Successfully!")

    return render(request, "administrator/add_blog.html")

def edit_blog(request,id):
    get_blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        blog_title = escape(request.POST['blog_title'])
        blog_content = escape(request.POST['blog_content'])

        get_blog.blog_title = blog_title
        get_blog.blog_content= blog_content
        get_blog.save()
        messages.success(request, "Blog details updated successfully!")

    return render(request, "administrator/edit_blog.html", {"blog": get_blog})

def edit_cover(request,id):
    get_blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        blog_cover = request.FILES.get('blog_cover')

        get_blog.blog_cover = blog_cover
        get_blog.save()
        messages.success(request, "Blog Cover updated successfully!")

    return render(request, "administrator/edit_cover.html", {"blog": get_blog})

def delete_blog(request,id):
    gn_details = get_object_or_404(Blog, id=id)
    gn_details.delete()
    return redirect('administrator:blogs')

def gallery(request):
    gallery_info = Gallery.objects.all()
    context = {
    "gallery_info": gallery_info,
    }
    return render(request, 'administrator/gallery.html', context)

def add_image(request):
    if request.method == "POST":
        gallery_cover = request.FILES.get('gallery_cover')
        insert_image = Gallery(gallery_cover=gallery_cover)
        insert_image.save()
        messages.success(request, "Gallery Added Successfully!")

    return render(request, "administrator/add_image.html")

def delete_image(request,id):
    gn_details = get_object_or_404(Gallery, id=id)
    gn_details.delete()
    return redirect('administrator:gallery')

def image_status(request,id,ssid):
    image_details = get_object_or_404(Gallery, id=id)
    if ssid == 1:
        image_details.gallery_sta = True
    else:
        image_details.gallery_sta = False
    image_details.save()
    return redirect('administrator:gallery')

def blog_status(request,id,ssid):
    image_details = get_object_or_404(Blog, id=id)
    if ssid == 1:
        image_details.blog_sta = True
    else:
        image_details.blog_sta = False
    image_details.save()
    return redirect('administrator:blogs')

def approve_result(request):
    term_info = get_object_or_404(Term,term_sta=True)
    session_info = get_object_or_404(Session,id=1)
    gt = term_info.term_name
    gs = session_info.session_name
    result_info = Grade.objects.select_related("grade_term").filter(
                    grade_term=gt,
                    grade_session=gs
                ).values('grade_sta','grade_term','grade_session').annotate(total=Count('id'))
    context = {
    "result_info": result_info,
    }
    return render(request, 'administrator/approve_result.html', context)

def approve_resultt(request, id):
    if id == 1:
        Grade.objects.update(grade_sta=True)
    else:
        Grade.objects.update(grade_sta=False)
    
    return redirect('administrator:approve_result')

def assignments(request):
    section_classes = Assign.objects.select_related("assign_teacher","assign_class")
    subject_teacher_info = Assign_subject.objects.select_related("assign_teacher","assign_subject")
    secthead = Assign_section.objects.select_related("assign_steacher","assign_section")
    context = {
        "section_classes": section_classes,
        "subject_teacher_info": subject_teacher_info,
        "secthead": secthead,
    }
    return render(request, "administrator/assignments.html", context)

def delete_ca(request,id):
    ca_details = get_object_or_404(Assign, id=id)
    ca_details.delete()
    return redirect('administrator:assignments')

def delete_sa(request,id):
    sa_details = get_object_or_404(Assign_subject, id=id)
    sa_details.delete()
    return redirect('administrator:assignments')

def delete_ssa(request,id):
    ssa_details = get_object_or_404(Assign_section, id=id)
    ssa_details.delete()
    return redirect('administrator:assignments')