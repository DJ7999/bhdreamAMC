# Generated by Django 4.2.5 on 2023-11-24 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "wealthwish_controller",
            "0003_remove_fire_monthly_contribution_current_cagr_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="fire",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
