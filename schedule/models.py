from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(auto_now_add=False)
    nickname_choice = (
        ('엄마','엄마'),
        ('아빠','아빠'),
        ('첫째','첫째'),
        ('둘째','둘째'),
        ('가족','가족'),
    )
    nickname = models.CharField(choices=nickname_choice, max_length=100, blank=True)
    memo = models.TextField(max_length=100, blank=True)
    history = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return self.name
        # return f'[{self.pk}]{self.name}'

    def get_absolute_url(self):
        return f'/person/{self.pk}/'

    def get_event_cnt(self):
        # reverse relation을 사용하여 연결된 Event 데이터의 갯수를 가져옴
        return self.event_set.count()


class Event(models.Model):
    personid = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, verbose_name='person')

    title = models.CharField(max_length=200)
    category_choice = (
        (0,'0 school: no school..'),
        (1,'1 class: math, bookclub, korean..'),
        (2,'2 EC: music, art, sports, volunteer..'),
        (3,'3 clinic'),
        (4,'4 social: party..'),
        (5,'5 todo'),
        (6,'6 etc'),
    )
    category = models.IntegerField(choices=category_choice, default=1)
    day_choice = (
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),
        (6,'Sunday'),
    )
    day = models.IntegerField(choices=day_choice, default=0)
    time = models.TimeField(null=True)
    duration = models.CharField(max_length=10, default='60')
    price = models.IntegerField(default=0)
    memo = models.TextField(max_length=100, blank=True)

    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/event/{self.pk}/'

    def get_schedule_cnt(self):
        # reverse relation을 사용하여 연결된 Schedule 데이터의 갯수를 가져옴
        return self.schedule_set.count()


class Schedule(models.Model):
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, verbose_name='event')
    personid = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, verbose_name='person')

    title = models.CharField(max_length=200, help_text='ex) S_piano  이름의 첫 알파벳과 함께 만들어 주세요!')
    day_choice = (
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),
        (6,'Sunday'),
    )
    day = models.IntegerField(choices=day_choice, default=0)
    date = models.DateTimeField(null=True, blank=True)
    dateday = models.DateField(null=True)
    datetime = models.TimeField(null=True)

    duration = models.CharField(max_length=10, default='60', help_text='분 단위로 입력해 주세요!')
    price = models.IntegerField(default=0)
    volunteerhours = models.CharField(default='0', max_length=10)
    bigevent = models.BooleanField(default=0)
    memo = models.TextField(max_length=100, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def get_absolute_url(self):
        url = reverse('schedule_update', args=[self.id])
        # ret_val = u'%s' % (str(self.id))

        if self.id == 0:
            color = "green"
        elif self.id == 1:
            color = "red"
        elif self.id == 2:
            color = "yellow"
        elif self.id == 3:
            color = "violet"
        else:
            color = "blue"


        ret_val = u'<font color="%s"><a href="%s">%s</a>' % (color, url, str(self.datetime.hour)+':'+str(self.datetime.minute)+' <b>'+str(self.title)+'</b></font>')

        # ret_val = u'<a href="%s">%s</a>' % (url, str(self.date.hour)+':'+str(self.date.minute)+' '+str(self.title))

        return ret_val

    def get_data_url(self):
        return f'/schedule/{self.pk}/'

    def get_schedule_event_title(self):
        return f'{self.eventid.title}'

    # def get_schedule_daylist(self):
    #     daylist = Schdeule.objects.filter(date_field(date)==date_field(self.date))
    #     return daylist

    # def get_daymenulist(self):
    #     menus = MyCalMenu.objects.filter(day=self.day)
    #     return menus


    # def __str__(self):
    #     return self.stitle



