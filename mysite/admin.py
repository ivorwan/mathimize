from django.contrib import admin
from django import forms
from mysite.models import Level
from mysite.models import Worksheet

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
    class Meta:
        model = Worksheet

class WorksheetAdmin(admin.ModelAdmin):
#    model = Worksheet
    list_display = ['worksheet_name', 'get_level_name', 'description', 'number_of_exercises', 'average_time']
    form = WorksheetAdminForm
    def get_level_name(self, obj):
        return obj.level.level_name
    get_level_name.short_description = 'Level'

admin.site.register(Level, LevelAdmin)
admin.site.register(Worksheet, WorksheetAdmin)



