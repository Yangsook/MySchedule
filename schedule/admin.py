from django.contrib import admin
from .models import Person, Event, Schedule

# admin.site.register(Person)
# admin.site.register(Event)
# admin.site.register(Schedule)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','personid','day','time','duration','price','startdate','enddate','active')
    list_filter = ['personid']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title','eventid','date','dateday','datetime','day','duration','price','volunteerhours')
    list_filter = ['personid','date']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified',
    )
    list_display = ('name','birthday','nickname')

    def person_actions(self, obj):
        pass
        # TODO: Render action buttons

