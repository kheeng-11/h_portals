# Generated by Django 5.1.7 on 2025-04-10 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0020_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade_ca',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade_exam',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade_total',
            field=models.FloatField(),
        ),
    ]
