from django import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm) :
      username = forms.CharField(max_length=50 , required=True)
      first_name =  forms.CharField(max_length=100, required=True)
      second_name = forms.CharField(max_length=100, required=True)
      email = forms.EmailField(max_length=250, help_text='exp example@gmail.com')

      class Meta :
           model = User
           fields = ( 'username','first_name' , 'second_name' , 'email' , 'password1' , 'password2')


