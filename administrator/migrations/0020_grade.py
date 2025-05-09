# Generated by Django 5.1.7 on 2025-04-10 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0019_exam_questions_question_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_submission_date', models.DateTimeField(auto_now_add=True)),
                ('grade_sta', models.BooleanField(default=False)),
                ('grade_approve_date', models.CharField(default='-', max_length=255)),
                ('grade_approve_comment', models.TextField(default='-')),
                ('grade_term', models.CharField(default='', max_length=255)),
                ('grade_session', models.CharField(default='', max_length=255)),
                ('grade_ca', models.CharField(default='', max_length=255)),
                ('grade_exam', models.CharField(default='', max_length=255)),
                ('grade_total', models.CharField(default='', max_length=255)),
                ('grade_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_class', to='administrator.class')),
                ('grade_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_student', to='administrator.students')),
                ('grade_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_subject', to='administrator.subject')),
            ],
        ),
    ]
