from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.conf import settings
from datetime import datetime
from pytz import timezone

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

            primary_contact = add_contact({
                'name': form.cleaned_data['submission_primary_name'],
                'email': form.cleaned_data['submission_primary_email']
            })
            secondary_contact = add_contact({
                'name': form.cleaned_data['submission_secondary_name'],
                'email': form.cleaned_data['submission_secondary_email']
            })

            if settings.DIGITAL_EDITION:
                digital_edition = DigitalEdition.objects.create(
                    showcase=form.cleaned_data['digital_showcase'],
                    new_this_year=form.cleaned_data['digital_what_is_new']
                )
            else:
                digital_edition = None

            late_submission = False
            submission_dt = datetime.now(tz=timezone('Europe/Brussels'))
            if submission_dt > settings.SUBMISSION_DEADLINE:
                late_submission = True

            submission = Submission.objects.create(
                fosdem_edition=settings.EDITION,
                project_id=project.id,
                justification=form.cleaned_data['submission_justification'],
                duration=form.cleaned_data['submission_duration'],
                primary_contact=primary_contact,
                primary_reason=form.cleaned_data['submission_primary_reason'],
                secondary_contact=secondary_contact,
                secondary_reason=form.cleaned_data['submission_secondary_reason'],
                notes=form.cleaned_data['submission_notes'],
                submission_date=submission_dt,
                submission_for_digital_edition=settings.DIGITAL_EDITION,
                digital_edition=digital_edition,
                late_submission=late_submission
            )
            return render(request, 'submission/received.html', {
                'project': project.name,
                'edition': submission.fosdem_edition
            })

    else:
        form = SubmissionForm()
    return render(request, 'submission/form.html', {
        'form': form,
        'digital_edition': settings.DIGITAL_EDITION
    })


def submit(request):
    pass


def add_contact(contact_data):
    try:
        contact = Contact.objects.get(email=contact_data['email'])
    except Contact.DoesNotExist:
        contact = Contact.objects.create(
            name=contact_data['name'],
            email=contact_data['email']
        )
    else:
        contact.name = contact_data['name']
        contact.save()
    return contact
