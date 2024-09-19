from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput, CheckboxSelectMultiple

from .models import Ad


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'name',
            'image',
            'description',
            'price',
            'category',
            'location',
            'start_date',
            'end_date',
            'phone'
        ]
        widgets = {
            'start_date':
                DateInput(attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
                ),
            'end_date':
                DateInput(attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'category':
                CheckboxSelectMultiple(attrs={
                    'class': 'form-control',
                })
        }


