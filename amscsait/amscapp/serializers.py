from rest_framework import serializers
from .models import Patient
from .models import Question


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('__all__')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('__all__')
