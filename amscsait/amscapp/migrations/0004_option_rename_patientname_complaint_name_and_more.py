# Generated by Django 4.0.4 on 2022-05-19 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amscapp', '0003_rename_choiceteset_question_choicetest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100, verbose_name='Вариант ответа')),
                ('score', models.IntegerField(default=0, verbose_name='Количество баллов')),
            ],
            options={
                'verbose_name': 'Поле для выбора',
                'verbose_name_plural': 'Поля для выборов',
            },
        ),
        migrations.RenameField(
            model_name='complaint',
            old_name='patientname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='fieldtest',
            new_name='fieldstest',
        ),
        migrations.RemoveField(
            model_name='question',
            name='choicetest',
        ),
        migrations.RenameModel(
            old_name='Field',
            new_name='Fields',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.AddField(
            model_name='option',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amscapp.fields'),
        ),
    ]
