from django.contrib import admin
from ...models import Review
from django.utils.html import format_html
from django.urls import reverse


class ReviewAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_description', 'theme', 'duration', 'justification',
                    'showcase', 'new_this_year', 'review', 'more_details', 'reviewed_by', 'current_score', 'accepted')

    def __init__(self, *args, **kwargs):
        super(SubmissionAdmin, self).__init__(*args, **kwargs)
        self.request = None

    def get_queryset(self, request):
        qs = super(SubmissionAdmin, self).get_queryset(request)
        self.request = request
        return qs

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

    def review(self, obj):
        _url = reverse('review_admin:review_review_add')
        is_change = False
        if self.request:
            if hasattr(obj, 'reviews') and obj.reviews:
                for review in obj.reviews.all():
                    if review.reviewer.id == self.request.user.id:
                        _url = reverse('review_admin:review_review_change', args=(review.id,))
                        is_change = True
                        break
        _prefilled_url = _url
        if self.request:
            if not is_change:
                _prefilled_url = '{0}?reviewer={1}&submission={2}'.format(
                    _url,
                    self.request.user.id,
                    obj.id
                )
        else:
            if not is_change:
                _prefilled_url = '{0}?submission={1}'.format(
                    _url,
                    obj.id
                )

        _html = '<a href="{0}">Review</a>'.format(
            _prefilled_url
        )

        return format_html(_html)

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
