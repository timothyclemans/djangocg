from djangocg.utils import timezone

from djangocg.db import models


def expensive_calculation():
    expensive_calculation.num_runs += 1
    return timezone.now()

class Poll(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=expensive_calculation)
