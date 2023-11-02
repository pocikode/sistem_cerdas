from django import forms

from .models import Job


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['account', 'keyword', 'limit', 'start_time', 'end_time']

    # account = forms.CharField()
    # keyword = forms.CharField()
    # limit = forms.IntegerField()
    # start_time = forms.DateTimeField()
    # end_time = forms.DateTimeField()
