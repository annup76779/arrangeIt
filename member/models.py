from django.db import models

from user.models import MemberUser


# Create your models here.

class Schedule(models.Model):
    member = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="schedule")
    start = models.DateTimeField()
    end = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    additional = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("start", )
