from django import forms
from .models import *


class LogInForm(forms.ModelForm):
    class Meta:
        model = LogIn
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['name', 'surname', 'email', 'password', 'repeat_password']
        widgets = {
            'password': forms.PasswordInput(),
            'repeat_password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        return surname

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("repeat_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

# First Parameter indicates the return value, sencond parameter indicates printed values to the web

EVENTS = (
    ('', 'Select Events'),
    ('All Events', 'All Events'),
    ('Cinema', 'Cinema'),
    ('Theatre', 'Theatre'),
    ('Opera', 'Opera'),
    ('Dance', 'Dance'),
)

CITIES = (
    ('', 'Select Cities'),
    ('All Cities', 'All Cities'),
    ('Istanbul', 'Istanbul'),
    ('Izmir', 'Izmir'),
    ('Bursa', 'Bursa'),
    ('Trabzon', 'Trabzon'),
)

SHOWROOMS = (
    ('', 'Select Showrooms'),
    ('All Showrooms', 'All Showrooms'),
    ('Jolly Joker Bursa', 'Jolly Joker Bursa'),
    ('Izmir Alsancak', 'Izmir Alsancak'),
    ('Kucuk Ciftlik Park', 'Kucuk Ciftlik Park'),
    ('Forum Trabzon', 'Forum Trabzon'),
)


class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['baturay'] = forms.ChoiceField(
            choices=EVENTS)


class CityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.ChoiceField(
            choices=CITIES)


class ShowroomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ShowroomForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.ChoiceField(
            choices=SHOWROOMS)
