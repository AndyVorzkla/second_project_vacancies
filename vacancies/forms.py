from django import forms
from vacancies import models


class PostcardForm(forms.Form):
    address = forms.CharField(label='Destination Address')
    author = forms.CharField(min_length=3)
    compliment = forms.CharField(max_length=1024)


class Application(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Submit'))
    #
    #     self.helper.form_class = 'card mt-4 mb-3'
    #     self.helper.label_class = 'mb-1 mt-2'
    #     self.helper.field_class = 'form-control'

    class Meta:
        model = models.Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {
            'written_username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'userName'
            }),
            'written_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'userPhone',
                'type': 'number',
            }),
            'written_cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'userMsg',
                'rows': 8
            })

        }


class Company(forms.ModelForm):
    # logo = forms.ImageField(
    #     widget=forms.FileInput(attrs={
    #         'class': 'custom-file-input',
    #         'type': 'file',
    #         'id': 'inputGroupFile01',
    #     })
    # )

    class Meta:
        model = models.Company
        fields = ('name', 'city', 'description', 'employee_count', 'logo')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'companyName',
                'type': 'text',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'companyLocation',
                'type': 'text',
            }),
            'logo_update': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file',
                'id': 'inputGroupFile01'
            }),

            'logo': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file',
                'id': 'inputGroupFile01',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'companyInfo',
                'style': 'color:#000;',
                'rows': 4
            }),
            'employee_count': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'companyTeam',
                'type': 'text',
            }),

        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = models.Vacancy
        fields = ('title', 'specialty', 'skills', 'text', 'salary_min', 'salary_max')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'vacancyTitle',
                'type': 'text',
            }),
            'specialty': forms.Select(attrs={
                'class': 'form-control',
                'id': 'userSpecialization',
            }),
            'salary_min': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'vacancySalaryMin',
                'type': 'text',
            }),
            'salary_max': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'vacancySalaryMax',
                'type': 'text',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vacancySkills',
                'style': 'color:#000;',
                'rows': 3
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vacancyDescription',
                'style': 'color:#000;',
                'rows': 13
            }),

        }
