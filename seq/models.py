from django.db import models
import uuid

# Create your models here.
class projects(models.Model):
    tag = models.ManyToManyField('tags', blank=True) #Tag is a string because it is above the Project model. The relationship is established in the orginial model. 

    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True,editable=False)

    def __str__(self):
        return self.title

class fiber(models.Model):
    project_relationship = models.ForeignKey(projects, on_delete=models.CASCADE)
    
    fib_title = models.CharField(max_length=200)
    fib_type = (
        ('24','24 COUNT'), 
        ('96','96 COUNT'),
        ('144','144 COUNT'),
        ('432','432 COUNT'),
        ('864','864 COUNT'),
    )
    fib_select = models.CharField(max_length=200, choices=fib_type)
    created_time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True,editable=False)

    def __str__(self):
        return self.fib_title 

class sequentials(models.Model):
    fiber_relationship = models.ForeignKey(fiber, on_delete=models.CASCADE)

    in_seq = models.IntegerField(null=True,blank=True)
    out_seq = models.IntegerField(null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True,editable=False)

    def __str__(self):
        return str(self.fiber_relationship) 


class tags(models.Model): 
    tag_name =  models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True,editable=False)

    def __str__(self):
        return self.tag_name 