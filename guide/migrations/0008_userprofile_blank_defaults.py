# Generated manually for UserProfile blank defaults

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0007_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="academic_year",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="department",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=120),
        ),
    ]
