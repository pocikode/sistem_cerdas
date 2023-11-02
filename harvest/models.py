from enum import Enum

from django.db import models


class JobStatus(Enum):
    WAITING = 'WAITING'
    PROCESS = 'PROCESS'
    DONE = 'DONE'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Account(models.Model):
    username = models.CharField(max_length=50)
    auth_token = models.CharField(max_length=100)


class Job(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    keyword = models.CharField(max_length=250)
    limit = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=25, choices=JobStatus.choices(), default=JobStatus.WAITING.value)

    def get_status_label(self):
        return JobStatus(self.status).name.title()
