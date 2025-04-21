from django import forms
from administrator.models import Parent

class ProfilePictureFormT(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['parent_picture']
