import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#    def __str__(self):
#        return str(self.question)
#    def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#    was_published_recently.admin_order_field = 'pub_date'
#    was_published_recently.boolean = True
#    was_published_recently.short_description = 'Published recently?'

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()
#    def __str__(self):
#        return str(self.choice)

class Level(models.Model):
    level_name = models.CharField(max_length=5, primary_key=True)
    def get_level_name(self):
        return self.level_name

class Worksheet(models.Model):
    worksheet_name = models.CharField(max_length=20, primary_key=True)
    level = models.ForeignKey(Level)
    description = models.CharField(max_length=2000)
    number_of_exercises = models.IntegerField()
    average_time = models.IntegerField()