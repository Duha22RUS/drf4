from . import views
from django.urls import path
from .views import SearchResultsView

urlpatterns = [
    path("", views.index, name="index"),
    path("new_patient", views.create_patient, name="create_patient"),
    path("patient/<int:pk>", views.view_patient, name="view_patient"),
    path("patient/<int:pk>/edit", views.edit_patient, name="edit_patient"),
    path("patient/<int:pk>/make_answers", views.make_answers, name="make_answers"),
    path("register", views.register, name="register"),
    path("login", views.user_login, name="login"),
    path("exit", views.exit, name="exit"),
    path('search/', SearchResultsView.as_view(), name='search'),
]
