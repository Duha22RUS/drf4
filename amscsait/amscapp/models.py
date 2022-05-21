from django.db import models


class Question(models.Model):
    name = models.CharField('Вопрос', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Option(models.Model):
    name = models.CharField('Вариант ответа', max_length=100)
    score = models.IntegerField('Количество баллов', default=0)
    option = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поле для выбора'
        verbose_name_plural = 'Поля для выборов'


class Patient(models.Model):
    class ChoiceSEX(models.TextChoices):
        MAN = 'Мужской', 'Мужской'
        WOMAN = 'Женский', 'Женский'

    class ChoiceNation(models.TextChoices):
        RU = 'Русские', 'Русские'
        UA = 'Украинцы', 'Украинцы'
        GE = 'Немцы', 'Немцы'
        KZ = 'Казахи', 'Казахи'
        BL = 'Белорусы', 'Белорусы'
        ALT = 'Алтайцы', 'Алтайцы'
        KU = 'Кумандинцы', 'Кумандинцы'
        TA = 'Татары', 'Татары'
        OT = 'Другая', 'Другая'

    name = models.CharField('ФИО', max_length=100)
    date_of_birth = models.DateField('Дата рождения')
    sex = models.CharField('Пол пациента', max_length=7, choices=ChoiceSEX.choices, default=1)
    insurance = models.CharField('Страховая организация', max_length=100, blank=True)
    policy = models.CharField('Страховое свидетельство', max_length=100, blank=True)
    address = models.CharField('Домашний адрес', max_length=100, blank=True)
    number_phone = models.CharField('Номер телефона', max_length=100, blank=True)
    email = models.EmailField('Электронная почта', max_length=100, blank=True)
    parent_name = models.CharField('ФИО родителя', max_length=100, blank=True)
    parent_number_phone = models.CharField('Номер телефона родителя', max_length=100, blank=True)
    parent_email = models.EmailField('Электронная почта родителя', max_length=100, blank=True)
    nation = models.CharField('Нация пациента', max_length=10, choices=ChoiceNation.choices, default=1)
    mother_nation = models.CharField('Нация матери пациента', max_length=10, choices=ChoiceNation.choices, default=1)
    father_nation = models.CharField('Нация отца пациента', max_length=10, choices=ChoiceNation.choices, default=1)
    registration_date = models.DateField('Дата регистрации пациента', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Complaint(models.Model):
    name = models.ForeignKey(to=Patient, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, default=1)
    option = models.ForeignKey(to=Option, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Анкетирование'
        verbose_name_plural = 'Анкетирования'