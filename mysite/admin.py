from django.contrib import admin
from django import forms
from django.forms import TextInput, Textarea
from django.db import models

from mysite.models import Level
from mysite.models import Worksheet
from mysite.models import WorksheetInt1Rules
from mysite.models import WorksheetInt2Rules
from mysite.models import DaysOfWeekSlot
from mysite.models import CalendarDaySlot
from mysite.models import Provider


class LevelAdmin(admin.ModelAdmin):
    model = Level
    list_display = ['level_name']
    list_filter = ['level_name']
    search_fields = ['level_name']


class LevelModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "level: %s" % (obj.get_level_name())



class WorksheetAdminForm(forms.ModelForm):
    level = LevelModelChoiceField(Level.objects.all())
    #description = forms.CharField(widget = forms.Textarea)
    class Meta:
        model = Worksheet
        widgets = {'description': forms.Textarea(attrs={'cols': '100'})}


class RulesForm(forms.ModelForm):
    class Meta:
        widgets = {'rule': forms.TextInput(attrs={'size': '175px'})}

class WorksheetInt1RulesInline(admin.TabularInline):
    model = WorksheetInt1Rules
    form = RulesForm
    extra = 1

class WorksheetInt2RulesInline(admin.TabularInline):
    model = WorksheetInt2Rules
    form = RulesForm
    extra = 1

class WorksheetAdmin(admin.ModelAdmin):
#    model = Worksheet
    list_display = ['worksheet_name', 'get_level_name', 'description', 'number_of_exercises', 'average_time']
    form = WorksheetAdminForm
#    def get_form(self, request, obj=None, **kwargs):
#        form = super(WorksheetAdmin, self).get_form(request, obj, **kwargs)
#        form.base_fields['description'].widget.attrs['style'] = 'width: 500px;'
#        return form
    def get_level_name(self, obj):
        return obj.level.level_name
    get_level_name.short_description = 'Level'
    inlines = [WorksheetInt1RulesInline, WorksheetInt2RulesInline]






############## ---------------------------------------------------------------------------------------------------

class DaysOfWeekSlotInline(admin.StackedInline):
    model = DaysOfWeekSlot
    extra = 0

class CalendarDaySlotInline(admin.TabularInline):
    model = CalendarDaySlot
    extra = 1

class ProviderAdmin(admin.ModelAdmin):
    class Media:
        #js = ('//code.jquery.com/ui/1.10.4/jquery-ui.js',)
        js = ('http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.5/jquery-ui.min.js',)
    def test(self):
        return ''


#class ProviderAdminForm(forms.ModelForm):

#class ProviderAdmin(admin.ModelAdmin):



admin.site.register(Level, LevelAdmin)
admin.site.register(Worksheet, WorksheetAdmin)

admin.site.register(DaysOfWeekSlot)
admin.site.register(CalendarDaySlot)
admin.site.register(Provider, ProviderAdmin)

