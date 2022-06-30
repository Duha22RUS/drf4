from datetime import date
from enum import Enum
import django
from django.contrib import auth
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class QuestionType(Enum):
    POLL = 'poll'
    TEXT = 'text'


class Question(models.Model):
    type_ = QuestionType.POLL
    question_number = models.IntegerField("Номер вопроса")
    question_text = models.CharField("Текст вопроса", max_length=100)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Вопрос с выбором ответа"
        verbose_name_plural = "Вопросы с выбором ответа"


class Option(models.Model):
    name = models.CharField("Вариант ответа", max_length=100)
    score = models.IntegerField("Колличество баллов", default=0)
    question = models.ForeignKey(
        "Question", related_name="options", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class TextQuestion(models.Model):
    type_ = QuestionType.TEXT
    question_number = models.IntegerField("Номер вопроса")
    question_text = models.CharField("Текст вопроса", max_length=100)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Текстовый вопрос"
        verbose_name_plural = "Текстовые вопросы"


class PatientTextAnswer(models.Model):
    # doctor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    patient = models.ForeignKey(to="Patient", on_delete=models.CASCADE)
    question = models.ForeignKey("TextQuestion", related_name="textquest", on_delete=models.CASCADE)
    answer = models.CharField("Ответ", max_length=100, blank=True)

    class Meta:
        verbose_name = "Ответ на текстовый вопрос"
        verbose_name_plural = "Ответы на текстовые вопросы"
        db_table = "amscapp_patienttextanswer"


class PatientAnswer(models.Model):
    # doctor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    patient = models.ForeignKey(to="Patient", on_delete=models.CASCADE)
    question = models.ForeignKey(to="Question", on_delete=models.CASCADE)
    option = models.ForeignKey(to="Option", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ анкеты"
        verbose_name_plural = "Ответы анкеты"
        db_table = "amscapp_patientanswer"


class Patient(models.Model):
    class GenderChoice(models.TextChoices):
        MAN = "Мужской", "Мужской"
        WOMAN = "Женский", "Женский"

    class NationChoice(models.TextChoices):
        RU = "Русские", "Русские"
        UA = "Украинцы", "Украинцы"
        GE = "Немцы", "Немцы"
        KZ = "Казахи", "Казахи"
        BL = "Белорусы", "Белорусы"
        ALT = "Алтайцы", "Алтайцы"
        KU = "Кумандинцы", "Кумандинцы"
        TA = "Татары", "Татары"
        OT = "Другая", "Другая"

    name = models.CharField("ФИО", max_length=100)
    date_of_birth = models.DateField("Дата рождения")
    gender = models.CharField(
        "Пол пациента", max_length=7, choices=GenderChoice.choices, default=GenderChoice.MAN
    )
    insurance = models.CharField("Наименование страховой организации", max_length=100, blank=True)
    policy = models.CharField("Страховое свидетельство", max_length=100, blank=True)
    address = models.CharField("Домашний адрес", max_length=100, blank=True)
    phone_number = models.CharField("Номер контактного телефона", max_length=100, blank=True)
    email = models.EmailField("Электронная почта", max_length=100, blank=True)
    parent_name = models.CharField("ФИО родителя/опекуна", max_length=100, blank=True)
    parent_phone_number = models.CharField(
        "Номер контактного телефона родителя/опекуна", max_length=100, blank=True
    )
    parent_email = models.EmailField(
        "Электронная почта родителя/опекуна", max_length=100, blank=True
    )
    nation = models.CharField(
        "Национальная принадлежность пациента",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    mother_nation = models.CharField(
        "Национальная принадлежность матери",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    father_nation = models.CharField(
        "Национальная принадлежность отца",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    date_registration = models.DateTimeField("Дата регистрации", auto_now_add=True)

    def __str__(self):
        return self.name

    def calculate_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
        db_table = "amscapp_patient"
