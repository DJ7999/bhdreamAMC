# Generated by Django 4.2.5 on 2023-11-24 03:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wealthwish_controller", "0002_remove_fire_monthly_contribution_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fire",
            name="monthly_contribution_current_cagr",
        ),
        migrations.RemoveField(
            model_name="fire",
            name="monthly_contribution_optimised_cagr",
        ),
    ]
