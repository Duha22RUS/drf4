from django.contrib import admin
from .models import Option, Patient, PatientAnswer, Question


class ChoiceInLineAdmin(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLineAdmin]


class PatientAnswerInLineAdmin(admin.TabularInline):
    model = PatientAnswer


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientAnswerInLineAdmin]
