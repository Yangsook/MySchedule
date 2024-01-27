"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from schedule import views
# import schedule.views

urlpatterns = [
    path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    # path('person/', views.PersonList.as_view(), name='person_list'),
    # path('person/<int:pk>/', views.PersonDetail.as_view(), name='person_detail'),
    # path('schedule/', views.ScheduleList.as_view(), name='schedule_list'),
    # path('schedule/<int:pk>/', views.ScheduleDetail.as_view(), name='schedule_detail'),

    path('calendar/<str:caldate>/schedule_create/', views.schedule_create, name='schedule_create'),
    path('calendar/<int:pk>/schedule_update/', views.schedule_update, name='schedule_update'),
    # path('calendar/<int:pk>/schedule_delete',
    #     views.schedule_delete.as_view(),
    #     name="schedule_delete",
    # ),


    path('person/', views.menu_person_list, name='person_add'),
    path('person/<int:pk>/', views.menu_person_edit, name='person_edit'),
    path('person/<int:pk>/delete', views.menu_person_delete, name='person_delete'),

    path('event/', views.menu_event_list, name='event_add'),
    path('event/<int:pk>/', views.menu_event_edit, name='event_edit'),
    path('event/<int:pk>/delete', views.menu_event_delete, name='event_delete'),

    path('schedule/', views.menu_schedule_list, name='schedule_add'),
    path('schedule/<int:pk>/', views.menu_schedule_edit, name='schedule_edit'),
    path('schedule/<int:pk>/delete', views.menu_schedule_delete, name='schedule_delete'),

    path('report/', views.menu_report_list, name='report_list'),
    path('report/search/', views.menu_report_search, name='report_search'),

    # path('person/', schedule.views.menu_person, name='person_list'),
    # path('event/', schedule.views.menu_event, name='event_list'),
    # path('schedule/', schedule.views.menu_schedule, name='schedule_list'),
    # path('report/', schedule.views.menu_report, name='report_list'),
]
