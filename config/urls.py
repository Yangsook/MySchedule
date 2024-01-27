from django.contrib import admin
from django.urls import path
from schedule import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('calendar/<str:caldate>/schedule_create/', views.schedule_create, name='schedule_create'),
    path('calendar/<int:pk>/schedule_update/', views.schedule_update, name='schedule_update'),

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
    path('report/monthlist/<int:eventid>/<str:year>/<str:month>',
         views.menu_report_monthlist, name='report_monthlist'),
]

