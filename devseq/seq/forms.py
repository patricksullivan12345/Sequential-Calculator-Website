from django.forms import ModelForm, HiddenInput, TextInput, NumberInput
from .models import projects, fiber, sequentials

class projectsForm(ModelForm):
    class Meta:
        model = projects
        fields = ['title','description']
        widgets = {
            
            'owner': HiddenInput(),

            'title': TextInput(attrs={
                'class': 'form_child_text',
                }),

            'description': TextInput(attrs={
                'class': 'form_child_textbox', 
                }),
        }

class fiberForm(ModelForm):
    class Meta:
        model = fiber
        fields = '__all__'
        widgets = {
            
            'project_relationship': HiddenInput(),

            'fib_title': TextInput(attrs={
                'class': 'form_child_text',
                }),
        } 

    def __init__(self, *args, **kwargs):
        super(fiberForm, self).__init__(*args, **kwargs)
        self.fields['fib_title'].label = "Please enter the fiber name:"
        self.fields['fib_select'].label = "What is the size of the fiber?"
        self.fields['fib_title'].required = False
        self.fields['fib_select'].required = False

class sequentialsForm(ModelForm):
    class Meta:
        model = sequentials
        fields = '__all__'
        widgets = {
            
            'fiber_relationship': HiddenInput(),
            
            'project_relationship': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(sequentialsForm, self).__init__(*args, **kwargs)
        self.fields['in_seq'].label = "In:"
        self.fields['out_seq'].label = "Out:"
        self.fields['in_seq'].widget.attrs.update({'class': 'form_child_number'})
        self.fields['out_seq'].widget.attrs.update({'class': 'form_child_number'})

           