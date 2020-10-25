from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.conf import settings

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            try:
                project = Project.objects.get(name=form.cleaned_data['project_name'])
            except Project.DoesNotExist:
                project = Project.objects.create(
                    name=form.cleaned_data['project_name'],
                    description=form.cleaned_data['project_description'],
                    theme_id=form.cleaned_data['project_theme'],
                    website=form.cleaned_data['project_website'],
                    social=form.cleaned_data['project_social'],
                    source=form.cleaned_data['project_source']
                )
            else:
                project.description = form.cleaned_data['project_description']
                project.theme_id = form.cleaned_data['project_theme']
                project.website = form.cleaned_data['project_website']
                project.social = form.cleaned_data['project_social']
                project.source = form.cleaned_data['project_source']
                project.save()
    else:
        form = SubmissionForm()
    return render(request, 'submission/form.html', {
        'form': form,
        'digital_edition': settings.DIGITAL_EDITION
    })


def submit(request):
    pass
