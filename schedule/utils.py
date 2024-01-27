from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Schedule
from django.urls import reverse

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.firstweekday=6
        self.events = events

        self.cssclasses = [style + " text-nowrap" for style in HTMLCalendar.cssclasses]
        self.cssclass_month_head = "text-center month-head "
        self.cssclass_month = "text-center month"
        self.cssclass_year = "text-italic lead"

    def formatday(self, day, weekday, events, theyear, themonth):
        """
        Return a day as a table cell.
        """


        if day == 0:
            args_day = datetime.date(year=theyear, month=themonth, day=1)
        else:
            args_day = datetime.date(year=theyear, month=themonth, day=day)

        day_url = reverse('schedule_create', args=[args_day])
        # day_url = ""

        events_from_day = events.filter(date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s"><a href="%s">%d</a>%s</td>' % (self.cssclasses[weekday], day_url, day, events_html)

    def formatweek(self, theweek, events, theyear, themonth):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, theyear, themonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, request, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Schedule.objects.filter(date__year=theyear, date__month=themonth)
        print(events)
        v = []
        a = v.append
        a('<table class="table" border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        # print('===== monthdays2calendar  ===')
        # print(self.monthdays2calendar(theyear, themonth))
        # print('===== monthdays2calendar  ===')
        for week in self.monthdays2calendar(theyear, themonth):
            print(week)
            a(self.formatweek(week, events, theyear, themonth))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

