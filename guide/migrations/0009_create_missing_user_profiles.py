# Data migration: create UserProfile for any User that does not have one

from django.db import migrations


def create_missing_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("guide", "UserProfile")
    for user in User.objects.all():
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "academic_year": "",
                "department": "",
                "email": user.email or "",
            },
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0008_userprofile_blank_defaults"),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles, noop),
    ]
