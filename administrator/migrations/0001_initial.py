# Generated by Django 5.1.7 on 2025-03-21 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_usermail', models.CharField(max_length=255)),
                ('admin_fname', models.CharField(max_length=255)),
                ('admin_othernames', models.CharField(max_length=255)),
                ('admin_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_email', models.CharField(max_length=255)),
                ('parent_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255)),
                ('section_added_on', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=255)),
                ('class_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.section')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_fname', models.CharField(max_length=255)),
                ('student_othernames', models.CharField(max_length=255)),
                ('student_adm', models.CharField(max_length=255)),
                ('student_password', models.CharField(max_length=255)),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_class', to='administrator.class')),
                ('student_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='administrator.parent')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=255)),
                ('subject_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.class')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_fname', models.CharField(max_length=255)),
                ('teacher_othernames', models.CharField(max_length=255)),
                ('teacher_email', models.CharField(max_length=255)),
                ('teacher_phone', models.CharField(max_length=255)),
                ('teacher_password', models.CharField(max_length=255)),
                ('teacher_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.section')),
            ],
        ),
        migrations.CreateModel(
            name='Assign_subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.subject')),
                ('assign_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.class')),
                ('assign_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.teacher')),
            ],
        ),
    ]
