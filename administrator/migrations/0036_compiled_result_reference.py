# Generated by Django 5.1.7 on 2025-04-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0035_compiled_result_sta'),
    ]

    operations = [
        migrations.AddField(
            model_name='compiled_result',
            name='reference',
            field=models.CharField(default='', max_length=255),
        ),
    ]
