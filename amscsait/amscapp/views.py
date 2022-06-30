from django.contrib.auth.models import User

from .forms import (AnswersForm, PatientForm, UserLoginForm,
                    UserRegisterForm)
from .models import Patient, PatientAnswer, TextQuestion, PatientTextAnswer
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(Q(name__icontains=query)
                                          | Q(date_of_birth__icontains=query)
                                          | Q(address__icontains=query)
                                          | Q(policy__icontains=query)
                                          | Q(phone_number__icontains=query))
    else:
        patients = Patient.objects.order_by("name")
    return render(request, "amscapp/index.html", {"patients": patients, "title": "Главная"})


@login_required
@permission_required('amscapp.add_patient', raise_exception=True)
def create_patient(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Пациент добавлен")
        return redirect("view_patient", pk=form.instance.pk)
    return render(
        request,
        "amscapp/post_form.html",
        {"form": form, "title": "Добавление пациента", "submit_text": "Добавить пациента"},
    )


@permission_required('amscapp.view_patient', raise_exception=True)
def view_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    answers = patient.patientanswer_set.all()
    textanswers = patient.patienttextanswer_set.all()
    total_score = patient.patientanswer_set.all().aggregate(
        total_score=Sum("option__score")
    )["total_score"]
    if patient.gender == patient.GenderChoice.MAN:
        total_score = patient.patientanswer_set.all().aggregate(
            total_score=Sum("option__score") + 1)["total_score"]
    return render(
        request,
        "amscapp/view_patient.html",
        {"patient": patient, "answers": answers, "textanswers": textanswers,
         "total": total_score, "title": "Анкета пациента"},
    )


@permission_required('amscapp.change_patient', raise_exception=True)
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.success(request, "Пациент изменен")
        return redirect("view_patient", pk=form.instance.pk)
    return render(
        request, "amscapp/post_form.html",
        {"form": form, "title": "Изменение пациента", "submit_text": "Применить изменения"}
    )


@permission_required('amscapp.change_patientanswer', raise_exception=True)
def make_answers(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = AnswersForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.success(request, "Ответы сохранены")
        return redirect("view_patient", pk=form.instance.pk)
    return render(
        request, "amscapp/post_form.html",
        {"form": form, "title": "Анкетирование", "submit_text": "Сохранить результаты"}
    )


@user_passes_test(lambda u: not u.is_authenticated)
def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно!")
        return redirect("index")
    return render(
        request, "amscapp/post_form.html", {"form": form, "title": "Регистрация", "submit_text": "Регистрация"}
    )


@user_passes_test(lambda u: not u.is_authenticated)
def user_login(request):
    form = UserLoginForm(request, request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Вы успешно вошли!")
        return redirect("index")
    return render(request, "amscapp/post_form.html", {"form": form, "title": "Авторизация", "submit_text": "Вход"})


@login_required
def exit(request):
    logout(request)
    return redirect("login")


def admin(request):
    return render(request, 'admin/')
