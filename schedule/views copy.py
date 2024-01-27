from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from .models import Person, Event, Schedule
from .forms import ScheduleForm, PersonForm, EventForm

import datetime
import calendar
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from .utils import EventCalendar

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

def menu_person_delete(request, pk):
    myPerson = get_object_or_404(Person, id=pk)
    myPerson.delete()
    return redirect('person_add')

def menu_event_delete(request, pk):
    myEvent = get_object_or_404(Event, id=pk)
    myEvent.delete()
    return redirect('event_add')


def menu_event_list(request):
    datalist = Event.objects.all().order_by('-active','day','time')

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
    datalist = Event.objects.all().order_by('id')
    myEvent = get_object_or_404(Event, id=pk)

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

        # return redirect('event_add')



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

    # if request.method == 'POST':
    #     form = ScheduleForm(request.POST)
    #     if form.is_valid():
    #         form.save(commit=False)
    #         dateday = request.POST.get('dateday')
    #         datetime = request.POST.get('datetime')

    #         print(dateday)
    #         print(datetime)

    #         form.date = dateday + " " + datetime
    #         form.save()

    #         # return render(request, 'index.html', {'move_mday':form.day})
    #         return redirect('home')
    # else:
    #     form = ScheduleForm()

    # return render(request, 'menu/schedule_create.html', {'form':form, 'caldate':caldate, 'daylist':daylist})
    # return render(request, 'event/mycalmenu.html', {'form':form, 'day':day, 'daymenulist':daymenulist})




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
            # return render(request, 'index.html', {'move_mday':form.day})
            return redirect('schedule_update', myschedule.pk)

        return redirect('home')


# def schedule_update(request, pk):

#     myschedule = Schedule.objects.get(id=pk)
#     print('pk: ' + str(pk))
#     print(myschedule)

#     caldate = str(myschedule.dateday)
#     daylist = Schedule.objects.filter(dateday__year=caldate[0:4],dateday__month=caldate[5:7],dateday__day=caldate[8:10])
#     print('caldate: ' + caldate)
#     print(daylist)

#     if request.method == 'GET':
#         form = ScheduleForm(instance = myschedule)
#         context = {
#             'myschedule': myschedule,
#             'form': form,
#             'daylist': daylist,
#         }
#         return render(request, 'menu/schedule_form.html', context)

#     elif request.method == 'POST':
#         pass


class schedule_delete(DeleteView):
    model = Schedule
    template_name = "menu/schedule_delete.html"
    success_url = reverse_lazy("home")
    # success_url = reverse_lazy("mycalmenu_list")



# def mycalmenu_list(request, day=None):
#     daymenulist = MyCalMenu.objects.filter(day=day)

#     if request.method == 'POST':
#         form = MyCalMenuForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.userid = 1 #request.userid
#             form.save()
#             return redirect('home')
#     else:
#         form = MyCalMenuForm()

#     return render(request, 'event/mycalmenu.html', {'form':form, 'day':day, 'daymenulist':daymenulist})


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
