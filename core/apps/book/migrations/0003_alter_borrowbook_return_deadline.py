# Generated by Django 5.1.5 on 2025-01-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowbook",
            name="return_deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
