# Generated by Django 4.2.5 on 2023-11-24 03:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wealthwish_controller", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fire",
            name="monthly_contribution",
        ),
        migrations.AddField(
            model_name="fire",
            name="monthly_contribution_current_cagr",
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name="fire",
            name="monthly_contribution_optimised_cagr",
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AlterField(
            model_name="goal",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
