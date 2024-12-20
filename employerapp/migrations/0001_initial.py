# Generated by Django 5.1.2 on 2024-12-07 05:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('qualifications', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('salary_range', models.CharField(blank=True, max_length=255, null=True)),
                ('job_type', models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('contract', 'Contract'), ('temporary', 'Temporary'), ('internship', 'Internship')], max_length=20)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('closing_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Post',
                'verbose_name_plural': 'Job Posts',
            },
        ),
    ]
