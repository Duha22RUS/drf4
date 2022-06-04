import django
from django.db import models


class Question(models.Model):
    question_text = models.CharField("Текст вопроса", max_length=100)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


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


class PatientAnswer(models.Model):
    patient = models.ForeignKey(to="Patient", on_delete=models.CASCADE)
    question = models.ForeignKey(to="Question", on_delete=models.CASCADE)
    option = models.ForeignKey(to="Option", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ анкеты"
        verbose_name_plural = "Ответ анкеты"


class Patient(models.Model):
    class GenderChoice(models.TextChoices):
        MAN = "Мужской", "Мужской"
        WOMAN = "Женский", "Женский"

    class NationChoice(models.TextChoices):
        RU = "Русский", "Русский"
        UA = "Украинец", "Украинец"
        GE = "Немец", "Немец"
        KZ = "Казах", "Казах"
        BL = "Белорус", "Белорус"
        ALT = "Алтаец", "Алтаец"
        KU = "Кумандинец", "Кумандинец"
        TA = "Татарин", "Татарин"
        OT = "Другая", "Другая"

    name = models.CharField("ФИО", max_length=100)
    date_of_birth = models.DateField("Дата рождения")
    gender = models.CharField(
        "Пол", max_length=7, choices=GenderChoice.choices, default=GenderChoice.MAN
    )
    insurance = models.CharField("Страховая организация", max_length=100, blank=True)
    policy = models.CharField("Страховое свидетельство", max_length=100, blank=True)
    address = models.CharField("Домашний адрес", max_length=100, blank=True)
    phone_number = models.CharField("Номер телефона", max_length=100, blank=True)
    email = models.EmailField("Электронная почта", max_length=100, blank=True)
    parent_name = models.CharField("ФИО родителя", max_length=100, blank=True)
    parent_phone_number = models.CharField(
        "Номер телефона родителя", max_length=100, blank=True
    )
    parent_email = models.EmailField(
        "Электронная почта родителя", max_length=100, blank=True
    )
    nation = models.CharField(
        "Национальность",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    mother_nation = models.CharField(
        "Национальность матери",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    father_nation = models.CharField(
        "Национальность отца",
        max_length=10,
        choices=NationChoice.choices,
        default=NationChoice.RU,
    )
    date_registration = models.DateField("Дата регистрации", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
