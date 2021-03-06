from django import forms

from .models import User, Rating


class SearchForm(forms.Form):
    query = forms.CharField()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class RateMovieForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

    def clean_rating(self):
        cd = self.cleaned_data
        if cd['rating'] < 0 or cd['rating'] > 10:
            raise forms.ValidationError('Rating must be between 0 and 10.')
        return cd['rating']
