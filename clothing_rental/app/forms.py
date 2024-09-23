from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput, CheckboxSelectMultiple

from .models import Ad, Category, AdComments, Order
from django.core.validators import MinValueValidator, MaxValueValidator


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


class SearchAdForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=Category.objects.all(), required=False)
    min_price = forms.DecimalField(max_digits=7, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=7, decimal_places=2, required=False)
    keywords = forms.CharField(max_length=255, required=False, help_text='List keywords separated by spaces, that are present in name or description')


class CommentAdForm(forms.ModelForm):
    class Meta:
        model = AdComments
        fields = [
            'comment'
        ]



class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'start_date',
            'end_date',
            'quantity',
            'comment'
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
                })

        }
