import datetime
from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager
from django import forms
import random

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Create your models here.

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#     def __str__(self):
#         return str(self.question)
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'
#
# class Choice(models.Model):
#     poll = models.ForeignKey(Poll)
#     choice = models.CharField(max_length=200)
#     votes = models.IntegerField()
#     def __str__(self):
#         return str(self.choice)

#====================================================================================
# business models
#====================================================================================

class Level(models.Model):
    level_name = models.CharField(max_length=5, primary_key=True)
    def get_level_name(self):
        return self.level_name



class Worksheet(models.Model):

    WORKSHEET_NAME_CHOICES = (
        ('Addition', 'Addition'),
        ('Subtraction', 'Subtraction'),
        ('Multiplication', 'Multiplication')
    )
    TEMPLATE_CHOICES = (
        ('TWOCOL', 'Two Columns, Single Line Operations'),
        ('THREECOL', 'Three Columns, Single Line Operations'),
        ('FOURCOL', 'Four Columns, Multiple Line Operations')
    )


    worksheet_name = models.CharField(max_length=20, choices=WORKSHEET_NAME_CHOICES)
    level = models.ForeignKey(Level)
    description = models.CharField(max_length=2000)
    number_of_exercises = models.IntegerField()
    average_time = models.IntegerField()
    tags = TaggableManager()

    min_int_1 = models.IntegerField()
    max_int_1 = models.IntegerField()
    min_int_2 = models.IntegerField()
    max_int_2 = models.IntegerField()

    worksheet_template = models.CharField(max_length=10, choices=TEMPLATE_CHOICES)

    def get_worksheet_name(self):
        return self.worksheet_name

    def getDifferentRandomTerm(self, term1, minInt, maxInt):
        newTerm = random.randint(minInt, maxInt)
        while (newTerm == term1):
            newTerm = random.randint(minInt, maxInt)
        return newTerm

    def getRandomInt(self, termName, minInt, maxInt, rules, rulesParams = {}):

        local_scope = {}

        local_scope['randomNumber'] = random.randint(minInt, maxInt)
        #local_scope['randomNumber'] = 12

        rulesParams[termName] = "local_scope['randomNumber']"
        #randomNumber = random.randint(minInt, maxInt)
        # the while loop is not very optimal, but is quite generic to find a proper term that meets the criteria intEval
        # also be careful with infinite loops (rules that cannot be satisfied)



        #exec("local_scope['randomNumber'] = (local_scope['randomNumber'] if local_scope['randomNumber'] % 10 > 6 else local_scope['randomNumber'] // 10 * 10 + ( 10 - local_scope['randomNumber'] % 4))", locals())


        for r in rules.all():
            statement = "local_scope['randomNumber'] = " + self.populateTags(r.rule, rulesParams)
            exec(statement, locals())

#        params = {"key1":"value1", "key2":"value2", "key3":"value3"}
#        originalString = "testing populated string k1: {{key1}}, k2: {{key2}}, k3: {{key3}}"
#        populatedString = self.populateTags(originalString, params)

#        while self.evalRules(randomNumber, rules.all(), rulesParams) == False:
#            randomNumber = random.randint(minInt, maxInt)
        return local_scope['randomNumber']

    def get_int_1_rules(self):
        # figure a BETTER WAY BETTER way to do this!!!!!!
        worksheet = Worksheet.objects.get(pk=self.id)
        return worksheet.worksheetint1rules_set

    def get_int_2_rules(self):
        # figure a BETTER WAY BETTER way to do this!!!!!!
        worksheet = Worksheet.objects.get(pk=self.id)
        return worksheet.worksheetint2rules_set

    def evalRules(self, randomNumber, rules, rulesParams):
        is_valid = True
        for r in rules.all():
            if eval(str(randomNumber) + r.rule) == False:
               is_valid = False
               break
        return  is_valid

    def populateTags(self, originalString, tagsDictionary):
        populatedString = originalString
        for k in tagsDictionary.keys():
            populatedString = populatedString.replace("{{" + k  + "}}", str(tagsDictionary[k]))
        return populatedString


class WorksheetInt1Rules(models.Model):
    worksheet = models.ForeignKey(Worksheet)
    rule = models.CharField(max_length=1000)

class WorksheetInt2Rules(models.Model):
    worksheet = models.ForeignKey(Worksheet)
    rule = models.CharField(max_length=1000)



########################################################################################################################################
#class DaysOfWeek(Enum):
#    Monday = 1
#    Tuesday = 2
#    Wednesday = 4
#    Thursday = 8

#DAYS_OF_WEEK = ((1, 'Monday'), (2, 'Tuesday'), (4, 'Wednesday'), (8, 'Thursday'), (16, 'Friday'), (32, 'Saturday'), (64, 'Sunday'))

#class Provider(models.Model):
#    name = models.CharField(max_length=30)
#    def __str__(self):
#        return str(self.name)
#    def get_blocked_days_of_week(self):
#        return

#class DaysOfWeekSlot(models.Model):
#    provider = models.ForeignKey(Provider)
#    weekday = models.IntegerField(choices=DAYS_OF_WEEK)
#    time = models.TimeField()
#    class Meta:
#        unique_together = (("provider", "weekday", "time"),)
#    def __str__(self):
#        return "%s - %s - %s" % (str(self.provider), str(self.weekday), str(self.time))

#class CalendarDaySlot(models.Model):
#    provider = models.ForeignKey(Provider)
#    date = models.DateField()
#    time = models.TimeField()
#    class Meta:
#        unique_together = (("provider", "date", "time"),)
#    def __str__(self):
#        return "%s - %s - %s" % (str(self.provider), str(self.date), str(self.time))






#====================================================================================
# form models
#====================================================================================
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '25', 'cols': '80', 'class': 'form-control', 'placeholder':'Enter Your Message'}))
    sender = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    cc_myself = forms.BooleanField(required=False)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        return self.cleaned_data.get('email')
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


