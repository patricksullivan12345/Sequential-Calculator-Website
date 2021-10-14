from django.forms import ModelForm, HiddenInput
from .models import projects, fiber, sequentials

class projectsForm(ModelForm):
    class Meta:
        model = projects
        fields = '__all__'

class fiberForm(ModelForm):
    class Meta:
        model = fiber
        fields = '__all__'
        widgets = {'project_relationship': HiddenInput()}

class sequentialsForm(ModelForm):
    class Meta:
        model = sequentials
        fields = '__all__'
        widgets = {'fiber_relationship': HiddenInput()}