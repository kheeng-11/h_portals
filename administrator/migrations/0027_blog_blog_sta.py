# Generated by Django 5.1.7 on 2025-04-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0026_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_sta',
            field=models.BooleanField(default=False),
        ),
    ]
