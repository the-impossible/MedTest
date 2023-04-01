import csv, io
from django import forms
from MedTest_auth.models import *

class FileHandler:
    def __init__(self, obj):
        self.csv_obj = obj

    def validate_stud_file(self):
        for col in self.csv_obj:
            existing_users = User.objects.filter(username=col[0])
            if len(col) != 2:raise forms.ValidationError('Invalid CSV FILE')
            for row in col:
                if row == '':raise forms.ValidationError('Invalid CSV, Missing DATA!!')
            if existing_users.exists():
                raise forms.ValidationError(f'File contains already registered registration number! {existing_users[0].username}')

class CreateStudentForm(forms.Form):
    file = forms.FileField(help_text='Select Student CSV file',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.csv'
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", required=True, help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    college = forms.ModelChoiceField(queryset=College.objects.all(), empty_label="(Select College)", required=True, help_text="Select College", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    # class Meta:
    #     model = StudentProfile
    #     fields = ('programme', 'session', 'college')

    def clean_file(self):

        file = io.TextIOWrapper(self.cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        # next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_stud_file()

        return file

