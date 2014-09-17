from django.db import models
from django.contrib.auth.models import User

import diff_utils




class Project(models.Model):
    url = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ReviewRequest(models.Model):
    project = models.ForeignKey(Project)
    description = models.TextField()
    diff = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def parsed_diff(self):
        # reload needed to clean parser data
        reload(diff_utils)
        return diff_utils.DiffParser(self.diff).parse()


class Reviewer(models.Model):
    user = models.ForeignKey(User)
    review_request = models.ForeignKey(ReviewRequest)
    accepted = models.BooleanField(default=False)
