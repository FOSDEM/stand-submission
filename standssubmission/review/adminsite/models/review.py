from django.contrib import admin
from ...models import Review
from django.utils.html import format_html
from django.urls import reverse


class ReviewAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ReviewAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['reviewer'].initial_value = 1
        form.base_fields['submission'].initial_value = 2
        return form


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_description', 'theme', 'duration', 'justification',
                    'showcase', 'new_this_year', 'review', 'more_details', 'reviewed_by', 'current_score', 'accepted')

    @staticmethod
    def project_name(obj):
        return obj.project.name

    @staticmethod
    def project_description(obj):
        return obj.project.description

    @staticmethod
    def theme(obj):
        return obj.project.theme.theme

    @staticmethod
    def showcase(obj):
        if hasattr(obj, 'digital_edition') and obj.digital_edition:
            return obj.digital_edition.showcase
        return ''

    @staticmethod
    def new_this_year(obj):
        if hasattr(obj, 'digital_edition') and obj.digital_edition:
            return obj.digital_edition.new_this_year
        return ''

    @staticmethod
    def review(obj):
        return format_html('<a href="{0}">Review</a>'.format(
            reverse('review_admin:review_review_add')
        ))

    @staticmethod
    def more_details(obj):
        return format_html('<a href="{0}">More details</a>'.format(
            reverse('admin:submission_submission_change', args=(obj.id,))
        ))

    @staticmethod
    def reviewed_by(obj):
        if hasattr(obj, 'reviews') and obj.reviews:
            return [
                r.reviewer.username for r in obj.reviews.all()
            ]
        return []

    @staticmethod
    def current_score(obj):
        if hasattr(obj, 'reviews') and obj.reviews:
            total = 0
            for r in obj.reviews.all():
                total = total + r.score
            return total
        return 0

    @staticmethod
    def accepted(obj):
        if hasattr(obj, 'decision') and obj.decision:
            return obj.decision.accepted
        return False
