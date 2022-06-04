from .models import Patient, PatientAnswer, Question
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"class": "datepicker"}),
        }


class AnswersForm(forms.Form):
    def __init__(self, *args, instance: Patient, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)
        questions = Question.objects.all()
        existing_answers = {
            question_id: option_id
            for question_id, option_id in PatientAnswer.objects.filter(
                patient=self.instance
            ).values_list("question_id", "option_id")
        }
        for question in questions:
            self.fields["question_%s" % question.id] = forms.ChoiceField(
                label=question.question_text,
                choices=question.options.all().values_list("id", "name"),
            )
            self.fields["question_%s" % question.id].initial = existing_answers.get(
                question.id, None
            )

    def save(self):
        answers_to_create = []
        for field, value in self.cleaned_data.items():
            question_id = field.split("_")[-1]
            answers_to_create.append(
                PatientAnswer(
                    patient=self.instance,
                    question_id=question_id,
                    option_id=value,
                )
            )
        PatientAnswer.objects.filter(patient=self.instance).delete()
        PatientAnswer.objects.bulk_create(answers_to_create)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
