# Generated by Django 5.1.3 on 2025-02-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_delete_pdfrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='codesubmission',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='codesubmission',
            name='pdf_generated',
            field=models.BooleanField(default=False),
        ),
    ]
