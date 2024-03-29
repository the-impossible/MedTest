# Generated by Django 4.1.7 on 2023-04-02 03:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("MedTest_auth", "0006_remove_studentprofile_department"),
    ]

    operations = [
        migrations.CreateModel(
            name="AmountToSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                (
                    "amount_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "Amount to schedule",
                "db_table": "Amount to schedule",
            },
        ),
        migrations.CreateModel(
            name="ScheduleTest",
            fields=[
                (
                    "test_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("has_expired", models.BooleanField(default=False)),
                ("test_date", models.DateTimeField()),
            ],
            options={
                "verbose_name_plural": "Schedule Tests",
                "db_table": "Schedule Test",
            },
        ),
        migrations.RemoveField(model_name="studentprofile", name="programme",),
        migrations.AddField(
            model_name="studentprofile",
            name="date_created",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(name="Programme",),
        migrations.AddField(
            model_name="scheduletest",
            name="stud_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="MedTest_auth.studentprofile",
            ),
        ),
    ]
