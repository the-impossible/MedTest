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

    college = forms.ModelChoiceField(queryset=College.objects.all(), empty_label="(Select College)", required=True, help_text="Select College", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean_file(self):

        file = io.TextIOWrapper(self.cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        # next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_stud_file()

        return file

class SingleCreateStudentForm(forms.ModelForm):

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    college = forms.ModelChoiceField(queryset=College.objects.all(), empty_label="(Select College)", required=True, help_text="Select College", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    username = forms.CharField(help_text='Enter Registration number',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter Registration number',
        }
    ))

    name = forms.CharField(help_text='Enter Full name',widget=forms.TextInput(
        attrs={
            'placeholder':'Enter Full name',
            'class':'form-control',
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise forms.ValidationError("Account already exist!")

        return username

    class Meta:
        model = User
        fields = ('username', 'name')

class ScheduleTestForm(forms.Form):

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    college = forms.ModelChoiceField(queryset=College.objects.all(), empty_label="(Select College)", required=True, help_text="Select College", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    test_date = forms.CharField(help_text='Enter Test date',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'datetime-local',
        }
    ))

class TestResultForm(forms.ModelForm):

    HB = forms.FloatField(help_text='HB G/100ML', required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number',
            'step':'0.01',
        }
    ))

    MP = forms.CharField(help_text='MP',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    DIFF = forms.CharField(help_text='DIFF',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    SNIP = forms.CharField(help_text='SNIP',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    SICKLING = forms.ModelChoiceField(queryset=Sickling.objects.all(), empty_label="(Select Sickling)", required=True, help_text="Select Sickling",  widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    GENOTYPE = forms.CharField(help_text='SNIP',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    GROUPING = forms.ModelChoiceField(queryset=BloodGroup.objects.all(), empty_label="(Select Blood Group)", required=True, help_text="Select Blood Group",  widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    SAG = forms.CharField(help_text='SAG',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    PREGNANCY = forms.CharField(help_text='PREGNANCY',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    REACTION = forms.CharField(help_text='REACTION',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    PROTEIN = forms.CharField(help_text='PROTEIN',required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    SUGAR = forms.CharField(help_text='SUGAR',required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    BILIRUBIN = forms.CharField(help_text='BILIRUBIN',required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    ACETONE = forms.CharField(help_text='ACETONE',required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    GRAVITY = forms.CharField(help_text='GRAVITY',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    U_PREGNANCY = forms.CharField(help_text='U_PREGNANCY',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    MICROSCOPY = forms.CharField(help_text='MICROSCOPY',required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))


    class Meta:
        model = TestResult
        fields = "__all__"
        exclude = ('stud_id', 'result_id' 'date_created')



