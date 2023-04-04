# Generated by Django 4.1.7 on 2023-04-04 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("MedTest_auth", "0017_scheduletest_result_uploaded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testresult",
            name="stud_id",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="MedTest_auth.studentprofile",
            ),
        ),
    ]
