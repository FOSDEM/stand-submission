from django.contrib import admin
from .models import Submission, Theme, Project, DigitalEdition, Contact, FOSDEMStandsEdition, FOSDEMEdition

# Register your models here.
admin.site.register(Submission)
admin.site.register(Theme)
admin.site.register(Project)
admin.site.register(DigitalEdition)
admin.site.register(Contact)
admin.site.register(FOSDEMEdition)
admin.site.register(FOSDEMStandsEdition)

