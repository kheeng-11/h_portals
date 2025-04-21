from django import forms
from .models import Students, Teacher, Parent

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        required=True,
        help_text=".xlsx only"
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")

        
        if not file.name.endswith(".xlsx"):
            raise forms.ValidationError("Only .xlsx files are allowed!")

        
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 5MB.")

        return file

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['student_picture']

class ProfilePictureFormT(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_picture']

class ProfilePictureFormP(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['parent_picture']