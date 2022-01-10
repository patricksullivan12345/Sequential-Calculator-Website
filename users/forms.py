from django.forms import ModelForm,HiddenInput,PasswordInput
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
 
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['email'].required = False
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form_child_text'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = { 'user': HiddenInput(),
                    'password1':PasswordInput(),
                    'password2':PasswordInput(),
                    } 

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['bio'].required = False

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form_child_text'})

        self.fields['bio'].widget.attrs.update({'class': 'form_child_textbox'})