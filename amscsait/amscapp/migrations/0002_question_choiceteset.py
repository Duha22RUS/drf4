# Generated by Django 4.0.4 on 2022-05-03 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amscapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choiceteset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='amscapp.choice'),
        ),
    ]
