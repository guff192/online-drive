from django import forms

from cloud.models import File


class CreateFileLinkForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('public',)
