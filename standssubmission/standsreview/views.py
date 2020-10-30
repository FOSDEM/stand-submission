from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from submission.models import Submission
from .models import Review, Decision
from .reviews.output import format_review
from .forms import *

# Create your views here.
login_url = '/review/login'


@login_required(login_url=login_url)
@permission_required('review.add_review', login_url=login_url)
def index_view(request):
    return render(request, 'standsreview/review.html', {})


@login_required(login_url=login_url)
@permission_required('review.add_review', login_url=login_url)
@api_view(['GET'])
def submission_api(request, edition=settings.EDITION):
    submissions = Submission.objects.filter(fosdem_edition=edition)
    formatted_submissions = []
    for submission in submissions:
        formatted_submission = {
            'id': submission.id,
            'project': submission.project.name,
            'description': submission.project.description,
            'justification': submission.justification
        }
        formatted_submissions.append(formatted_submission)
    return JsonResponse({
        'page': 1,
        'per_page': len(formatted_submissions),
        'total': len(formatted_submissions),
        'results': formatted_submissions
    })


@login_required(login_url=login_url)
@permission_required('review.add_review', login_url=login_url)
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def review_api(request, submission_id, review_id=None):
    submission = get_object_or_404(Submission, id=submission_id)
    if not review_id:
        if request.method == 'GET':
            formatted_reviews = []
            for review in submission.reviews_set.all():
                formatted_reviews.append(format_review(review))
            return JsonResponse({
                'page': 1,
                'per_page': len(formatted_reviews),
                'total': len(formatted_reviews),
                'results': formatted_reviews
            })
        elif request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = Review.objects.create(
                    submission=submission,
                    reviewer=request.user,
                    comments=form.cleaned_data['comments'],
                    score=form.cleaned_data['score']
                )
                return JsonResponse(format_review(review))
            else:
                return Response({'msg': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'Invalid parameter.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        if request.method == 'GET':
            pass
        elif request.method == 'PUT':
            pass
        elif request.method == 'DELETE':
            pass
        else:
            return Response({'msg': 'Invalid parameter.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required(login_url=login_url)
@permission_required('decision.add_decision', login_url=login_url)
@api_view(['GET', 'PUT'])
def decision_api(request):
    pass


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if form.cleaned_data['next_url']:
                    # Redirect
                    return redirect(form.cleaned_data['next_url'])
                else:
                    # Redirect to base
                    return redirect('index')
            else:
                return render(request, 'standsreview/login.html', {
                    'form': form,
                    'error': 'Invalid username or password.'
                })
        else:
            return render(request, 'standsreview/login.html', {
                'form': form,
                'error': 'Invalid username or password.'
            })
    else:
        try:
            next_url = request.GET['next']
        except KeyError:
            next_url = None
        form = LoginForm({
            'next_url': next_url
        })
        return render(request, 'standsreview/login.html', {
            'form': form
        })
