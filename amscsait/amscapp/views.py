from django.db.models import Q
from rest_framework import generics
from django.shortcuts import render, redirect
from .models import Patient, Option, Question
from .serializers import PatientSerializer, QuestionSerializer
from .forms import PatientForm, UserRegisterForm, UserLoginForm, OptionForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout


class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientSerializer


class PatientAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class QuestionAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# class DatabaseAPIView(generics.ListAPIView):
#    queryset = Patient.objects.order_by('name')
#    serializer_class = DatabaseSerializer


def database_home(request):
    database = Patient.objects.order_by('name')
    return render(request, 'database/database_home.html', {'database': database})


def add_patient(request):
    error = ''
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('database_home')
        else:
            error = 'Ошибка добавления'

    form = PatientForm()
    data = {'form': form, 'error': error}
    return render(request, 'database/add_patient.html', data)


def add_complaint(request):
    error = ''
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('database_home')
        else:
            error = 'Ошибка добавления'

    compla = Question.objects.order_by('name')
    # score = Option.objects.order_by('score')
    # ball = Option.objects.filter(option_id=score)
    form = OptionForm()
    data = {'form': form, 'error': error, 'compla': compla}
    return render(request, 'database/add_complaint.html', data)


def load_option(request):
    option_id = request.GET.get('name')
    option = Option.objects.filter(option_id=option_id).order_by('name')
    return render(request, 'database/city_dropdown_list_options.html', {'option': option})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('database_home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'database/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('database_home')
    else:
        form = UserLoginForm()
    return render(request, 'database/login.html', {"form": form})


def exit(request):
    logout(request)
    return redirect('login')


class SearchResultsView(ListView):
    model = Patient
    template_name = 'database/search_result.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Patient.objects.filter(Q(name__icontains=query))
        return object_list
