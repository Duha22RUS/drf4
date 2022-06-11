from django.contrib import admin
from .models import Option, Patient, PatientAnswer, Question, TextQuestion


class ChoiceInLineAdmin(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLineAdmin]


class PatientAnswerInLineAdmin(admin.TabularInline):
    model = PatientAnswer
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientAnswerInLineAdmin]


admin.site.register(TextQuestion)
