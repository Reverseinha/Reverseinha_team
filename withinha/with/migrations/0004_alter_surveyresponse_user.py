# Generated by Django 5.0.3 on 2024-07-29 09:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('with', '0003_alter_myuser_options_remove_myuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='survey_responses', to=settings.AUTH_USER_MODEL),
        ),
    ]
