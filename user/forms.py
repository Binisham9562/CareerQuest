# user/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # Override save method to hash the password securely
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set the password securely
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'autofocus', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']
