from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('api/submissions', views.submission_api, name='submission_api'),
    path('api/submissions/<str:edition>', views.submission_api, name='submission_api'),
    path('api/review/submission/<str:submission_id>/review', views.review_api, name='review_api'),
    path('api/review/submission/<str:submission_id>/review/<str:review_id>', views.review_api, name='review_api')
]
