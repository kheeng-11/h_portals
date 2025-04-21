from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'parent'

urlpatterns = [
	path('',home,name='home'),
	path('login/', login,name='login'),
	path('logout/', logout,name='logout'),
	path('profile/<int:id>/', profile, name='profile'),
	path('change_profile_picture/<int:id>/', change_profile_picture, name='change_profile_picture'),
	path('edit_profile/<int:id>/', edit_profile, name='edit_profile'),
	path('change_password/<int:id>/', change_password, name='change_password'),
	path('my_children/<int:id>/', my_children, name='my_children'),
	path('payment_record/<int:id>/', payment_record, name='payment_record'),
	path('student_payment_record/<int:id>/', student_payment_record, name='student_payment_record'),
	path('student_payment_reciept/<int:id>/',student_payment_reciept ,name='student_payment_reciept'),
	path('compiled_result/<int:id>/',compiled_result ,name='compiled_result'),
	path('print_result/<int:id>/',print_result ,name='print_result'),
]
