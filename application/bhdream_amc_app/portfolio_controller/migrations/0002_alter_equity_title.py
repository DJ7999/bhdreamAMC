# Generated by Django 4.2.5 on 2023-11-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio_controller", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equity",
            name="title",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
