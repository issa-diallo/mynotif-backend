# Generated by Django 5.0.9 on 2024-11-03 20:00

from django.db import migrations

from main.migrations_helpers import apply_rls_on_additional_tables

table_names = (
    "auth_group_permissions",
    "auth_user_groups",
    "auth_user_user_permissions",
    "django_migrations",
    "nurse_nurse_patients",
)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_rls_on_additional_tables(table_names)),
    ]
