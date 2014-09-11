from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Project, Reviewer, ReviewRequest


def home(request, project=None):
    requests = ReviewRequest.objects.all()

    return render(request, 'home.html', locals())


def review(request, review_id):
    pass


@csrf_exempt
def upload_review(request):
    project_id = request.POST['project_id']
    diff = request.POST['diff']
    description = request.POST['description']
    reviewers = request.POST['reviewers'].split(',')

    users = User.objects.filter(username__in=reviewers)
    if len(reviewers) != users.count():
        return HttpResponse('Reviewers error')

    review_request = ReviewRequest(project_id=project_id, diff=diff, description=description)
    review_request.save()
    for user in users:
        reviewer = Reviewer(user=user, review_request=review_request)
        reviewer.save()

    return HttpResponse('Review uploaded')
