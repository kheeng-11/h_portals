from django import forms
from administrator.models import Teacher

class ProfilePictureFormT(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_picture']
