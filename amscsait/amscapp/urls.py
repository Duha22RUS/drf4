from django.contrib import admin
from django.urls import path, include
from amscapp.views import PatientCreateView, PatientRUDView, SearchResultsView
from . import views

from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.database_home, name='database_home'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('exit', views.exit, name='exit'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_complaint', views.add_complaint, name='add_complaint'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('createpatient/', PatientCreateView.as_view()),
    path('detailpatient/<int:pk>/', PatientRUDView.as_view()),
    path('ajax/load-option/', views.load_option, name='ajax_load_option'),
]
