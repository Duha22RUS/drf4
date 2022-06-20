from django.contrib import admin
from django.contrib.auth.models import User
from import_export.widgets import ForeignKeyWidget

from .models import Option, Patient, PatientAnswer, Question, TextQuestion, PatientTextAnswer
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


class ChoiceInLineAdmin(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLineAdmin]


class PatientAnswerInLineAdmin(admin.TabularInline):
    model = PatientAnswer
    extra = 0


class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    inlines = [PatientAnswerInLineAdmin]
    resource_class = PatientResource


class PatientTextAnswerResource(resources.ModelResource):
    id = fields.Field(column_name='id', attribute='id')
    patient = fields.Field(column_name='Пациент', attribute='patient', widget=ForeignKeyWidget(Patient, 'name'))
    question = fields.Field(column_name='Вопрос', attribute='question',
                            widget=ForeignKeyWidget(TextQuestion, 'question_text'))
    answer = fields.Field(column_name='Ответ', attribute='answer')
    doctor = fields.Field(column_name='Врач', attribute='doctor', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = PatientTextAnswer


class PatientTextAnswerAdmin(ImportExportModelAdmin):
    resource_class = PatientTextAnswerResource


class PatientAnswerResource(resources.ModelResource):
    id = fields.Field(column_name='id', attribute='id')
    patient = fields.Field(column_name='Пациент', attribute='patient', widget=ForeignKeyWidget(Patient, 'name'))
    question = fields.Field(column_name='Вопрос', attribute='question',
                            widget=ForeignKeyWidget(Question, 'question_text'))
    option = fields.Field(column_name='Ответ', attribute='option',
                          widget=ForeignKeyWidget(Option, 'name'))
    doctor = fields.Field(column_name='Врач', attribute='doctor', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = PatientAnswer


class PatientAnswerAdmin(ImportExportModelAdmin):
    resource_class = PatientAnswerResource


admin.site.register(PatientTextAnswer, PatientTextAnswerAdmin)
admin.site.register(PatientAnswer, PatientAnswerAdmin)
admin.site.register(TextQuestion)
