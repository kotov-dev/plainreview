#encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Project, Reviewer, ReviewRequest



def home(request, project=None):
    pass
    requests = ReviewRequest.objects.order_by('-created_at').all()
    if project is not None:
        requests = requests.filter(project_id=project)
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
