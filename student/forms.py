from django import forms
from administrator.models import Students

class ProfilePictureFormT(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['student_picture']
