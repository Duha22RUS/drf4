from django.contrib import admin
from .models import Patient, Question, Option, Complaint


class ChoiceInLineAdmin(admin.TabularInline):
    model = Option


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLineAdmin]


admin.site.register(Patient)
admin.site.register(Complaint)
admin.site.register(Question, QuestionAdmin)