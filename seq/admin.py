from django.contrib import admin

# Register your models here.
from seq.models import projects, fiber, sequentials

admin.site.register(projects)
admin.site.register(fiber)
admin.site.register(sequentials)

