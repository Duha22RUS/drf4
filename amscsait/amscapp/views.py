from datetime import date
from django.http import HttpResponse
from .forms import (AnswersForm, PatientForm, UserLoginForm,
                    UserRegisterForm)
from .models import Patient, PatientAnswer, TextQuestion
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView


def sample_view(request):
    html = '<body><h1>Django sample_view</h1><br><p>Отладка sample_view</p></body>'
    return HttpResponse(html)


def index(request):
    patients = Patient.objects.order_by("name")
    return render(request, "amscapp/index.html", {"patients": patients})


@login_required
def create_patient(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Пациент добавлен")
        return redirect("view_patient", pk=form.instance.pk)
    return render(
        request,
        "amscapp/post_form.html",
        {"form": form, "title": "Добавление пациента"},
    )


def view_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    date = PatientAnswer.date_of_the_survey
    answers = patient.patientanswer_set.all()
    total_score = patient.patientanswer_set.all().aggregate(
        total_score=Sum("option__score")
    )["total_score"]
    return render(
        request,
        "amscapp/view_patient.html",
        {"patient": patient, "date": date, "answers": answers, "total": total_score},
    )


def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.success(request, "Пациент изменен")
        return redirect("view_patient", pk=form.instance.pk)
    return render(
        request, "amscapp/post_form.html", {"form": form, "title": "Изменение пациента"}
    )


def make_answers(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = AnswersForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.success(request, "Ответы сохранены")
        return redirect("view_patient", pk=form.instance.pk)
    return render(request, "amscapp/post_form.html", {"form": form})


@user_passes_test(lambda u: not u.is_authenticated)
def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно!")
        return redirect("index")
    return render(
        request, "amscapp/post_form.html", {"form": form, "title": "Регистрация"}
    )


@user_passes_test(lambda u: not u.is_authenticated)
def user_login(request):
    form = UserLoginForm(request, request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Вы успешно вошли!")
        return redirect("index")
    return render(request, "amscapp/post_form.html", {"form": form, "title": "Вход"})


@login_required
def exit(request):
    logout(request)
    return redirect("login")


class SearchResultsView(ListView):
    model = Patient
    template_name = 'amscapp/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Patient.objects.filter(Q(name__icontains=query))
        return object_list
