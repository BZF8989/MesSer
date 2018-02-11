# accounts.forms.py
from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        qs = User.objects.filter(phone_number=phone_number)
        if qs.exists():
            raise forms.ValidationError("phone number is taken")
        return phone_number

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def create_user(self, email, phone_number, password):
        return self.User.UserManager.create_user(email, phone_number, password)
