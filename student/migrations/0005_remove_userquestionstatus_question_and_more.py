# Generated by Django 5.1.3 on 2025-02-09 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_question_alter_user_admission_no_userquestionstatus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquestionstatus',
            name='question',
        ),
        migrations.RemoveField(
            model_name='userquestionstatus',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='admission_no',
        ),
        migrations.AddField(
            model_name='user',
            name='admission_number',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='QuestionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('code', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('status', models.CharField(default='Incomplete', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='UserQuestionStatus',
        ),
    ]
