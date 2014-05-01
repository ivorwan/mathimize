import datetime
from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager
from django import forms
import random


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
    worksheet_name = models.CharField(max_length=20)
    level = models.ForeignKey(Level)
    description = models.CharField(max_length=2000)
    number_of_exercises = models.IntegerField()
    average_time = models.IntegerField()
    tags = TaggableManager()
    def get_worksheet_name(self):
        return self.worksheet_name
    def getDifferentRandomTerm(self, term1, minInt, maxInt):
        newTerm = random.randint(minInt, maxInt)
        while (newTerm == term1):
            newTerm = random.randint(minInt, maxInt)
        return newTerm

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '25', 'cols': '80', 'class': 'form-control', 'placeholder':'Enter Your Message'}))
    sender = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    cc_myself = forms.BooleanField(required=False)

