from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from .models import Person, Event, Schedule
from .forms import ScheduleForm, PersonForm, EventForm
from django.db.models import Count, Sum, Q, F, Value
from django.db.models.functions import Extract
import datetime
import calendar
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from .utils import EventCalendar


############## Report Manager ##############
def menu_report_list(request):
    # datalist = Schedule.objects.values('personid','title','dateday__year','dateday__month').annotate(cnt=Count('id'), sum_price=Sum('price'), sum_volhours=Sum('volunteerhours')).order_by('personid')
    datalist = Schedule.objects.annotate(
        cnt=Count('id'),
        sum_price=Sum('price'),
        sum_volhours=Sum('volunteerhours')
    ).order_by('personid').values('personid', 'eventid__category', 'title', 'dateday__year', 'dateday__month', 'cnt', 'sum_price', 'sum_volhours')

    print(datalist)

    personlist = Person.objects.all()

    if request.method == "GET":
        context = { 'personlist':personlist, 'datalist':datalist }
        return render(request, 'menu/report_list.html', context)
    else:
        pass


def menu_report_search(request):
    myPerson = Person.objects.all()

    # Initial queryset
    query = Schedule.objects.values('personid', 'eventid__category', 'eventid', 'personid__name', 'title', 'dateday__year', 'dateday__month') \
        .annotate(cnt=Count('id'), sum_price=Sum('price'), sum_volhours=Sum('volunteerhours'))


    if request.method == "POST":
        selperson = request.POST.get('selperson', "")
        start_date = request.POST.get('start_date', "")
        end_date = request.POST.get('end_date', "")

        # Check conditions and modify query accordingly
        if selperson:
            if selperson and start_date and end_date:  # Case 2
                query = query.filter(personid=selperson, dateday__gte=start_date, dateday__lte=end_date)
            elif selperson and start_date:  # Case 5
                query = query.filter(personid=selperson, dateday__gte=start_date)
            elif selperson and end_date:  # Case 6
                query = query.filter(personid=selperson, dateday__lte=end_date)
            elif selperson:  # Case 3
                query = query.filter(personid=selperson)
            # elif start_date and end_date:  # Case 4
            #     query = query.filter(dateday__gte=start_date, dateday__lte=end_date)
        else:
            if start_date and end_date:  # Case 2
                query = query.filter(dateday__gte=start_date, dateday__lte=end_date)
            elif start_date:  # Case 5
                query = query.filter(dateday__gte=start_date)
            elif end_date:  # Case 6
                query = query.filter(dateday__lte=end_date)


        datalist = query.all()
        print(datalist)

        context = {'personlist': myPerson, 'selperson': selperson, 'start_date': start_date, 'end_date': end_date,
                   'datalist': datalist}
        return render(request, 'menu/report.html', context)
    else:

        datalist = query.all()
        context = {'personlist': myPerson, 'datalist': datalist}
        return render(request, 'menu/report.html', context)


def menu_report_monthlist(request, eventid, year, month):
    datalist = Schedule.objects.filter(eventid=eventid, dateday__year=year, dateday__month=month)
    print(datalist)

    # Calculate the sums of 'price', 'duration', and 'volunteerhours' fields
    totals = datalist.aggregate(
        total_price = Sum('price'),
        total_duration = Sum('duration'),
        total_volunteerhours = Sum('volunteerhours')
    )

    context = {'datalist': datalist, **totals}
    return render(request, 'menu/report_monthlist.html', context)

# def menu_report_search(request):
#     myPerson = Person.objects.all()

#     if request.method == "POST":
#         selperson = request.POST.get('selperson', "")

#         if selperson:
#             datalist = Schedule.objects.values('personid','title','dateday__year','dateday__month').annotate(cnt=Count('id'), sum_price=Sum('price'), sum_volhours=Sum('volunteerhours')).filter(personid=selperson)
#         else:
#             datalist = Schedule.objects.values('personid','title','dateday__year','dateday__month').annotate(cnt=Count('id'), sum_price=Sum('price'), sum_volhours=Sum('volunteerhours'))

#         print(datalist)

#         context = { 'personlist':myPerson, 'selperson':selperson, 'datalist':datalist }
#         return render(request, 'menu/report.html', context)

#     else:
#         datalist = Schedule.objects.values('personid','title','dateday__year','dateday__month').annotate(cnt=Count('id'), sum_price=Sum('price'), sum_volhours=Sum('volunteerhours'))
#         print(datalist)

#         context = { 'personlist':myPerson, 'datalist':datalist }
#         return render(request, 'menu/report.html', context)


# def home(request):
#     return render(request, 'index.html')

# class PersonList(ListView):
#     model = Person
#     ordering = '-pk'
#     template_name = 'menu/person_list.html'

# class PersonDetail(DetailView):
#     model = Person
#     template_name = 'menu/person_detail.html'

# class ScheduleList(ListView):
#     model = Schedule
#     ordering = '-pk'
#     template_name = 'menu/Schedule_list.html'

# class ScheduleDetail(DetailView):
#     model = Schedule
#     template_name = 'menu/Schedule_detail.html'


############## Person Manager
def menu_person_list(request):
    datalist = Person.objects.all().order_by('id')

    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_add')
    else:
        form = PersonForm()
        context = { 'form':form,'datalist':datalist }
        return render(request, 'menu/Person.html', context)


def menu_person_edit(request, pk):

    datalist = Person.objects.all().order_by('id')
    myPerson = get_object_or_404(Person, id=pk)

    if request.method == "GET":
        form = PersonForm(instance = myPerson)
        context = { 'form':form, 'datalist':datalist }
        return render(request, 'menu/Person.html', context)
    else:
        form = PersonForm(request.POST, instance = myPerson)

        if form.is_valid(): # cleaned_data를 사용하려면 유효성 검사가 필요하다. 유효성 검사를 통과한 데이터들만 사용할 수 있다.
            form.save()
            return redirect('person_add')
        else:
            return redirect('Person_edit', myPerson.pk)

        # return redirect('person_add')


############## Event Manager
def menu_event_list(request):
    datalist = Event.objects.all().order_by('-active', 'personid','day','time')

    # datalist = Event.objects.values(
    #     'id', 'title', 'category', 'day', 'time', 'duration', 'price', 'memo', 'active',
    #     'personid', 'personid__name'
    # ).order_by('-active', 'personid', 'day', 'time')

    # # 각 이벤트에 대한 절대 URL 가져오기
    # for event in datalist:
    #     event_instance = Event.objects.get(pk=event['id'])
    #     event['get_absolute_url'] = reverse('event_edit', args=[str(event_instance.id)])

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_add')
    else:
        form = EventForm()
        context = { 'form':form,'datalist':datalist }
        return render(request, 'menu/event.html', context)


def menu_event_edit(request, pk):
    datalist = Event.objects.all().order_by('-active', 'personid','day','time')
    # datalist = Event.objects.values(
    #     'id', 'title', 'category', 'day', 'time', 'duration', 'price', 'memo', 'active',
    #     'personid', 'personid__name'
    # ).order_by('-active', 'personid', 'day', 'time')

    myEvent = get_object_or_404(Event, id=pk)
    print(datalist)

    if request.method == "GET":
        form = EventForm(instance = myEvent)
        context = { 'form':form, 'datalist':datalist }
        return render(request, 'menu/event.html', context)
    else:
        form = EventForm(request.POST, instance = myEvent)

        if form.is_valid(): # cleaned_data를 사용하려면 유효성 검사가 필요하다. 유효성 검사를 통과한 데이터들만 사용할 수 있다.
            form.save()
            return redirect('event_add')
        else:
            return redirect('event_edit', myEvent.pk)


############## Schedule Manager ##############
def menu_schedule_list(request):
    datalist = Schedule.objects.all().order_by('-dateday','-datetime')

    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # form.save()
            Schedule.objects.create(
                personid = form.cleaned_data['personid'],
                eventid = form.cleaned_data['eventid'],
                title = form.cleaned_data['title'],
                day = form.cleaned_data['day'],
                dateday = form.cleaned_data['dateday'],
                datetime = form.cleaned_data['datetime'],
                duration = form.cleaned_data['duration'],
                price = form.cleaned_data['price'],
                volunteerhours = form.cleaned_data['volunteerhours'],
                bigevent = form.cleaned_data['bigevent'],
                memo = form.cleaned_data['memo'],

                date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),

            )

            return redirect('schedule_add')
    else:
        form = ScheduleForm()
        context = { 'form':form,'datalist':datalist }
        return render(request, 'menu/schedule.html', context)


def menu_schedule_edit(request, pk):
    datalist = Schedule.objects.all().order_by('-dateday','-datetime')
    mySchedule = get_object_or_404(Schedule, id=pk)

    if request.method == "GET":
        form = ScheduleForm(instance = mySchedule)
        context = { 'form':form, 'datalist':datalist }
        return render(request, 'menu/schedule.html', context)
    else:
        form = ScheduleForm(request.POST, instance = mySchedule)

        if form.is_valid(): # cleaned_data를 사용하려면 유효성 검사가 필요하다. 유효성 검사를 통과한 데이터들만 사용할 수 있다.
            # form.save()
            myschedule = form.save(commit=False)

            personid = form.cleaned_data['personid']
            eventid = form.cleaned_data['eventid']
            title = form.cleaned_data['title']
            day = form.cleaned_data['day']
            dateday = form.cleaned_data['dateday']
            datetime = form.cleaned_data['datetime']
            duration = form.cleaned_data['duration']
            price = form.cleaned_data['price']
            volunteerhours = form.cleaned_data['volunteerhours']
            bigevent = form.cleaned_data['bigevent']
            memo = form.cleaned_data['memo']

            date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),


            # myschedule.date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),
            myschedule = form.save()
            return redirect('schedule_add')
        else:
            return redirect('schedule_edit', mySchedule.pk)




##############  delete  ##############
def menu_person_delete(request, pk):
    myPerson = get_object_or_404(Person, id=pk)
    myPerson.delete()
    return redirect('person_add')

def menu_event_delete(request, pk):
    myEvent = get_object_or_404(Event, id=pk)
    myEvent.delete()
    return redirect('event_add')

def menu_schedule_delete(request, pk):
    mySchedule = get_object_or_404(Schedule, id=pk)
    mySchedule.delete()
    return redirect('schedule_add')





############## Calender manager ##############
def schedule_create(request, caldate=None):
    daylist = Schedule.objects.filter(dateday__year=caldate[0:4],dateday__month=caldate[5:7],dateday__day=caldate[8:10])
    print('caldate: ' + caldate)
    print(daylist)


    if request.method == "GET":
        form = ScheduleForm()
        context = { 'form':form, 'caldate':caldate, 'daylist':daylist }
        return render(request, 'menu/schedule_create.html', context)
    else:
        form = ScheduleForm(request.POST)

        if form.is_valid(): # cleaned_data를 사용하려면 유효성 검사가 필요하다. 유효성 검사를 통과한 데이터들만 사용할 수 있다.
            Schedule.objects.create(
                personid = form.cleaned_data['personid'],
                eventid = form.cleaned_data['eventid'],
                title = form.cleaned_data['title'],
                day = form.cleaned_data['day'],
                dateday = form.cleaned_data['dateday'],
                datetime = form.cleaned_data['datetime'],
                duration = form.cleaned_data['duration'],
                price = form.cleaned_data['price'],
                volunteerhours = form.cleaned_data['volunteerhours'],
                bigevent = form.cleaned_data['bigevent'],
                memo = form.cleaned_data['memo'],

                date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),

            )
        else:
            # return render(request, 'index.html', {'move_mday':form.day})
            return redirect('home')

        return redirect('home')


def schedule_update(request, pk):
    myschedule = get_object_or_404(Schedule, id=pk)
    print('myschedule.personid: ' + str(myschedule.personid))
    print(myschedule)

    caldate = str(myschedule.dateday)
    daylist = Schedule.objects.filter(dateday__year=caldate[0:4],dateday__month=caldate[5:7],dateday__day=caldate[8:10])
    print('caldate: ' + caldate)
    print(daylist)

    if request.method == "GET":
        form = ScheduleForm(instance = myschedule)
        context = { 'form':form, 'caldate':{'caldate':caldate}, 'daylist':daylist }
        return render(request, 'menu/schedule_form.html', context)
    else:
        form = ScheduleForm(request.POST, instance = myschedule)

        if form.is_valid(): # cleaned_data를 사용하려면 유효성 검사가 필요하다. 유효성 검사를 통과한 데이터들만 사용할 수 있다.
            myschedule = form.save(commit=False)

            personid = form.cleaned_data['personid']
            eventid = form.cleaned_data['eventid']
            title = form.cleaned_data['title']
            day = form.cleaned_data['day']
            dateday = form.cleaned_data['dateday']
            datetime = form.cleaned_data['datetime']
            duration = form.cleaned_data['duration']
            price = form.cleaned_data['price']
            volunteerhours = form.cleaned_data['volunteerhours']
            bigevent = form.cleaned_data['bigevent']
            memo = form.cleaned_data['memo']

            date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),


            # myschedule.date = str(form.cleaned_data['dateday']) + " " + str(form.cleaned_data['datetime']),
            myschedule = form.save()
        else:
            return redirect('schedule_update', myschedule.pk)

        return redirect('home')


class schedule_delete(DeleteView):
    model = Schedule
    template_name = "menu/schedule_delete.html"
    success_url = reverse_lazy("home")
    # success_url = reverse_lazy("mycalmenu_list")



############## Home  ##############
def home(request, extra_context=None):
    move_mday = request.GET.get('move_mday', None)
    extra_context = extra_context or {}

    if not move_mday:
        d = datetime.date.today()
    else:
        try:
            split_move_mday = move_mday.split('-')
            d = datetime.date(year=int(split_move_mday[0]), month=int(split_move_mday[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                    day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)  # find first day of next month

    extra_context['previous_month'] = reverse('home') + '?move_mday=' + str(previous_month)
    extra_context['next_month'] = reverse('home') + '?move_mday=' + str(next_month)

    cal = EventCalendar()
    html_calendar = cal.formatmonth(request, d.year, d.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    extra_context["calendar"] = mark_safe(html_calendar)

    # print('=======  user =======')
    # print(request.user)
    # print('=======  user =======')
    return render(request, 'index.html', extra_context)
