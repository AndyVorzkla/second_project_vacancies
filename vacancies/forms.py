from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from vacancies.models import *


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
        model = Application
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


