from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Admin(models.Model):
    admin_usermail = models.CharField(max_length=255)
    admin_fname = models.CharField(max_length=255)
    admin_othernames = models.CharField(max_length=255)
    admin_password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.admin_password.startswith('pbkdf2_sha256$'):
            self.admin_password = make_password(self.admin_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.admin_password)

    def __str__(self):
        return self.admin_usermail

class Section(models.Model):
	section_name = models.CharField(max_length=255)
	section_added_on = models.CharField(max_length=255)

	def __str__(self):
		return self.section_name

class Class(models.Model):
	class_name = models.CharField(max_length=255)
	class_section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Teacher(models.Model):
    teacher_fname = models.CharField(max_length=255)
    teacher_othernames = models.CharField(max_length=255)
    teacher_email = models.CharField(max_length=255)
    teacher_phone = models.CharField(max_length=255)
    teacher_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    teacher_password = models.CharField(max_length=255)
    teacher_dob = models.CharField(max_length=255, default='')
    teacher_picture = models.ImageField(upload_to="teacher_pictures/", default="teacher_pictures/default.jpg")
    teacher_address = models.CharField(max_length=255, default='')
    teacher_gender = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        if not self.teacher_password.startswith('pbkdf2_sha256$'):
            self.teacher_password = make_password(self.teacher_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.teacher_password)

    def __str__(self):
        return self.teacher_email

class Subject(models.Model):
	subject_name = models.CharField(max_length=255)
	subject_class = models.ForeignKey(Class , on_delete=models.CASCADE)

	def __str__(self):
		return self.subject_name

class Assign(models.Model):
    assign_teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE)
    assign_class = models.ForeignKey(Class , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.assign_teacher} -> {self.assign_class}"

class Assign_subject(models.Model):
    assign_teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE)
    assign_subject = models.ForeignKey(Subject , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.assign_teacher} -> {self.assign_subject}"

class Parent(models.Model):
    parent_email = models.CharField(max_length=255)
    parent_password = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255, default='')
    parent_address = models.CharField(max_length=255, default='')
    parent_phone = models.CharField(max_length=255, default='')
    parent_picture = models.ImageField(upload_to="parent_pictures/", default="parent_pictures/default.jpg")

    def save(self, *args, **kwargs):
        if not self.parent_password.startswith('pbkdf2_sha256$'):
            self.parent_password = make_password(self.parent_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.parent_password)

    def __str__(self):
        return self.parent_email

class Students(models.Model):
    student_fname = models.CharField(max_length=255)
    student_othernames = models.CharField(max_length=255)
    student_adm = models.CharField(max_length=255)
    student_parent = models.ForeignKey(Parent , on_delete=models.CASCADE, related_name='parent')
    student_password = models.CharField(max_length=255)
    student_class = models.ForeignKey(Class , on_delete=models.CASCADE,related_name='student_class')
    student_dob = models.CharField(max_length=255, default='')
    student_picture = models.ImageField(upload_to="student_pictures/", default="student_pictures/default.jpg")
    student_address = models.CharField(max_length=255, default='')
    student_gender = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        if not self.student_password.startswith('pbkdf2_sha256$'):
            self.student_password = make_password(self.student_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.student_password)

    def __str__(self):
        return self.student_fname

class Assign_section(models.Model):
    assign_steacher = models.ForeignKey(Teacher , on_delete=models.CASCADE)
    assign_section = models.ForeignKey(Section , on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.assign_steacher} -> {self.assign_section}"

class Notifications(models.Model):
    notification_content = models.TextField()
    notification_class = models.ForeignKey(Class , on_delete=models.CASCADE,related_name='notification_class')
    notification_date = models.DateTimeField(auto_now_add=True)
    notification_subject = models.ForeignKey(Subject , on_delete=models.CASCADE,related_name='notification_subject')

    def __str__(self):
        return self.notification_content

class Assignment(models.Model):
    assignment_date = models.DateTimeField(auto_now_add=True)
    assignment_instruction = models.TextField()
    assignment_material = models.FileField(upload_to='assignments_materials/')
    assignment_deadline = models.CharField(max_length=255)
    assignment_class = models.ForeignKey(Class , on_delete=models.CASCADE, related_name='assignment_class')
    assignment_subject = models.ForeignKey(Subject , on_delete=models.CASCADE, related_name='assignment_subject')
    assignment_sta = models.BooleanField(default=True)

    def __str__(self):
        return self.assignment_instruction

class Assignment_submission(models.Model):
    submission_assignment = models.ForeignKey(Assignment , on_delete=models.CASCADE, related_name='submission_assignment')
    submission_student = models.ForeignKey(Students , on_delete=models.CASCADE, related_name='submission_student')
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_material = models.FileField(upload_to='assignments_submission_materials/')
    submission_comment = models.TextField(default='-')

    def __str__(self):
        return self.submission_date

class Exam_questions(models.Model):
    question_subject = models.ForeignKey(Subject , on_delete=models.CASCADE, related_name='question_subject')
    question_class = models.ForeignKey(Class , on_delete=models.CASCADE, related_name = 'question_class')
    question_teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE, related_name = 'question_teacher')
    question_submission_date = models.DateTimeField(auto_now_add=True)
    question_material = models.FileField(upload_to='question_papers/')
    question_sta = models.BooleanField(default=False)
    question_approve_date = models.CharField(max_length=255, default='-')
    question_approve_comment = models.TextField(default='-')
    question_term = models.CharField(max_length=255,default='')
    question_session = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.question_submission_date

class Term(models.Model):
    term_name = models.CharField(max_length=255)
    term_sta = models.BooleanField(default=False)

    def __str__(self):
        return self.term_name

class Session(models.Model):
    session_name = models.CharField(max_length=255)

    def __str__(self):
        return self.session_name

class Grade(models.Model):
    grade_subject = models.ForeignKey(Subject , on_delete=models.CASCADE, related_name='grade_subject')
    grade_class = models.ForeignKey(Class , on_delete=models.CASCADE, related_name = 'grade_class')
    grade_student = models.ForeignKey(Students , on_delete=models.CASCADE, related_name = 'grade_student')
    grade_submission_date = models.DateTimeField(auto_now_add=True)
    grade_sta = models.BooleanField(default=False)
    grade_approve_date = models.CharField(max_length=255, default='-')
    grade_approve_comment = models.TextField(default='-')
    grade_term = models.CharField(max_length=255,default='')
    grade_session = models.CharField(max_length=255,default='')
    grade_ca = models.FloatField()
    grade_exam = models.FloatField()
    grade_total = models.FloatField()

    def __str__(self):
        return self.grade_session

class Payment(models.Model):
    payment_student = models.ForeignKey(Students , on_delete=models.CASCADE, related_name = 'payment_student')
    payment_term = models.CharField(max_length=255)
    payment_session = models.CharField(max_length=255)
    payment_description = models.TextField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_amount

class Events(models.Model):
    event_name = models.CharField(max_length=255)
    event_term = models.CharField(max_length=255)
    event_session = models.CharField(max_length=255)
    event_date = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name

class General_notification(models.Model):
    g_not_audience = models.CharField(max_length=255)
    g_not_date = models.DateTimeField(auto_now_add=True)
    g_not_notification = models.TextField()
    g_not_term = models.CharField(max_length=255,default='')
    g_not_session = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.g_not_audience

class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    blog_date = models.DateTimeField(auto_now_add=True)
    blog_content = models.TextField()
    blog_cover = models.ImageField(upload_to="blog_pictures/")
    blog_sta = models.BooleanField(default=False)
    blog_term = models.CharField(max_length=255,default='')
    blog_session = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.blog_title

class Gallery(models.Model):
    gallery_cover = models.ImageField(upload_to="gallery/")
    gallery_sta = models.BooleanField(default=False)

    def __str__(self):
        return self.gallery_cover

