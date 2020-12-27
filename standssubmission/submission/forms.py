from django import forms
from .models import Theme, Submission, DURATION_CHOICES, FOSDEMStandsEdition
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime, date
from pytz import timezone


class SubmissionForm(forms.Form):
    ##
    # Project information
    ##
    project_name = forms.CharField(label='Project name')
    project_description = forms.CharField(widget=forms.Textarea, label='Project description')
    project_theme = forms.ChoiceField(label='Project theme',
                                      choices=[
                                          (theme.id, theme.theme)
                                          for theme in Theme.objects.all()
                                      ])
    project_website = forms.URLField(label='Project website')
    project_source = forms.URLField(label='Source code')
    project_social = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Social media links'
    )

    ##
    # Submission information
    ##
    submission_justification = forms.CharField(widget=forms.Textarea, label='Why do you want to be at FOSDEM?')
    submission_duration = forms.ChoiceField(
        label='Do you want a stand for the entire event or just one day?',
        choices=DURATION_CHOICES
    )
    submission_primary_name = forms.CharField(label='Primary contact person')
    submission_primary_email = forms.EmailField(label='Primary contact person e-mail')
    submission_primary_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='What is the relation between the project and the primary contact?'
    )
    submission_secondary_name = forms.CharField(label='Secondary contact person')
    submission_secondary_email = forms.EmailField(label='Secondary contact person e-mail')
    submission_secondary_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='What is the relation between the project and the secondary contact?'
    )
    submission_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Anything to add?',
        required=False
    )

    ##
    # Digital edition?
    ##
    digital_edition = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    digital_showcase = forms.CharField(
        widget=forms.Textarea,
        label='Please enter a short (10 lines) description of why people should come to your stand.'
              ' This will be added to your stand on the overview website.'
    )
    digital_what_is_new = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 15}),
        label='Please enter a short (15 lines) overview of all the new things for your project since your last FOSDEM'
              ' and anything new to expect this year. This will be added to your stand on the overview website.'
    )

    def clean(self):
        cleaned_data = super().clean()
        try:
            edition = FOSDEMStandsEdition.objects.get(edition__year=settings.EDITION)
        except Exception as e:
            raise ValidationError(
                _('Submissions for FOSDEM are not open yet.')
            )
        if not edition.submissions_open:
            now_dt = date.today()
            if edition.deadline < now_dt:
                raise ValidationError(
                    _('Submissions for FOSDEM {0} are no longer open.'.format(
                        edition.edition.year
                    ))
                )
            else:
                raise ValidationError(
                    _('Submissions for FOSDEM {0} are not open yet.'.format(
                        edition.edition.year
                    ))
                )
        if cleaned_data.get('project_name'):
            submissions = Submission.objects.filter(
                project__name=cleaned_data.get('project_name'),
                edition=edition
            )
            if submissions:
                raise ValidationError(
                    _('Project {0} has already submitted a proposal for FOSDEM {1}.'.format(
                        cleaned_data.get('project_name'),
                        edition.edition.year
                    ))
                )
        return cleaned_data
