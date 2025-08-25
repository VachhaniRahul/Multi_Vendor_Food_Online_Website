from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        print(cleaned_data)
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error("password", "Passwords do not match")
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data
