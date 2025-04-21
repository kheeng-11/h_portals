from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'student'

urlpatterns = [
	path('',home,name='home'),
	path('login/', login,name='login'),
	path('logout/', logout,name='logout'),
	path('profile/<int:id>/', profile, name='profile'),
	path('change_profile_picture/<int:id>/', change_profile_picture, name='change_profile_picture'),
	path('edit_profile/<int:id>/', edit_profile, name='edit_profile'),
	path('change_password/<int:id>/', change_password, name='change_password'),
	path('my_record/<int:id>/', my_record, name='my_record'),
	path('payment_reciept/<int:id>/', payment_reciept, name='payment_reciept'),
	path('assignments/<int:id>/', assignments, name='assignments'),
	path('submissions/<int:id>/', submissions, name='submissions'),
	path('submit_assignment/<int:id>/', submit_assignment, name='submit_assignment'),
	path('delete_submission/<int:id>/', delete_submission, name='delete_submission'),
	path('compiled_result/<int:id>/', compiled_result, name='compiled_result'),
	path('print_result/<int:id>/', print_result, name='print_result'),
]
