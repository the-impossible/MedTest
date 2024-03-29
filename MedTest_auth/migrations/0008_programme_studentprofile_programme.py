# Generated by Django 4.1.7 on 2023-04-02 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("MedTest_auth", "0007_amounttoschedule_scheduletest_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Programme",
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
                ("programme_title", models.CharField(max_length=50, unique=True)),
                (
                    "programme_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"verbose_name_plural": "Programmes", "db_table": "Programme",},
        ),
        migrations.AddField(
            model_name="studentprofile",
            name="programme",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="MedTest_auth.programme",
            ),
            preserve_default=False,
        ),
    ]
