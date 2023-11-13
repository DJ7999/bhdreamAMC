# Generated by Django 4.2.5 on 2023-11-12 12:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_controller", "0004_alter_investment_principal_amount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="investment",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="investment",
            name="equity_symbol",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="user",
        ),
        migrations.DeleteModel(
            name="EquitySymbol",
        ),
        migrations.DeleteModel(
            name="Investment",
        ),
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]