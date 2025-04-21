from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import submit_score

app_name = 'teacher'

urlpatterns = [
	path('',home,name='home'),
	path('login/',login ,name='login'),
	path('logout/',logout ,name='logout'),
	path('my_classes/<int:id>/', my_classes, name='my_classes'),
	path('view_mystudents/<int:id>/<int:sid>/', view_mystudents, name='view_mystudents'),
	path('notifications/<int:id>/<int:sid>/', notifications, name='notifications'),
	path('add_notification/<int:id>/<int:sid>/', add_notification, name='add_notification'),
	path('delete_notification/<int:id>/', delete_notification, name='delete_notification'),
	path('edit_notification/<int:id>/<int:sid>/', edit_notification, name='edit_notification'),
	path('assignments/<int:id>/<int:sid>/', assignments, name='assignments'),
	path('add_assignment/<int:id>/<int:sid>/', add_assignment, name='add_assignment'),
	path('delete_assignment/<int:id>/', delete_assignment, name='delete_assignment'),
	path('edit_assignment/<int:id>/', edit_assignment, name='edit_assignment'),
	path('assignment_status/<int:id>/<int:ssid>/', assignment_status, name='assignment_status'),
	path('assignment_submission/<int:id>/', assignment_submission, name='assignment_submission'),
	path('exam_questions/<int:id>/', exam_questions, name='exam_questions'),
	path('submitted_questions/<int:id>/<int:sid>/', submitted_questions, name='submitted_questions'),
	path('add_exam_question/<int:id>/<int:sid>/', add_exam_question, name='add_exam_question'),
	path('delete_question/<int:id>/', delete_question, name='delete_question'),
	path('score_sheet/<int:id>/', score_sheet, name='score_sheet'),
	path('add_grade/<int:id>/<int:sid>/', add_grade, name='add_grade'),
	path('submit_score/<int:student_id>/', submit_score, name='submit_score'),
	path('m_class_students/<int:id>/', m_class_students, name='m_class_students'),
	path('student_record/<int:id>/', student_record, name='student_record'),
	path('profile/<int:id>/', profile, name='profile'),
	path('change_profile_picture/<int:id>/', change_profile_picture, name='change_profile_picture'),
	path('edit_profile/<int:id>/', edit_profile, name='edit_profile'),
	path('change_password/<int:id>/', change_password, name='change_password'),
	path('compiled_result/<int:id>/', compiled_result, name='compiled_result'),
	path('print_result/<int:id>/', print_result, name='print_result'),
]
