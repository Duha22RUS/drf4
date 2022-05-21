# Generated by Django 4.0.4 on 2022-05-19 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amscapp', '0006_alter_field_options_complaint_field_complaint_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.RenameField(
            model_name='option',
            old_name='field',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='field',
        ),
        migrations.AddField(
            model_name='complaint',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='amscapp.question'),
        ),
        migrations.AlterField(
            model_name='option',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amscapp.question'),
        ),
        migrations.DeleteModel(
            name='Field',
        ),
    ]