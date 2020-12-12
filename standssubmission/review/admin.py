from django.contrib import admin
from django.conf import settings
from .adminsite.models.review import ReviewAdmin, SubmissionAdmin
from .models import Review
from submission.models import Submission

# Register your models here.


class ReviewAdminSite(admin.AdminSite):
    site_header = 'FOSDEM stands review'
    site_title = 'FOSDEM {0} stands review'.format(settings.EDITION)
    index_title = 'Welcome to the FOSDEM stands review site'


review_admin_site = ReviewAdminSite(name='review_admin')


review_admin_site.register(Submission, SubmissionAdmin)
review_admin_site.register(Review, ReviewAdmin)
