from django.contrib.contenttypes.models import ContentType
from django.db import connection


def enable_rls_for_table_sql(table_name):
    """Returns a list of SQL commands to enable RLS for a given table."""
    return [
        f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;",
        # f"CREATE POLICY select_own_records ON {table_name} "
        # "FOR SELECT USING (user_id = auth.uid());",
        f"ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY;",
    ]


def enable_rls_on_tables(schema_editor, table_names):
    """
    Enables RLS on the specified tables by executing the relevant SQL commands.
    Only applies to PostgreSQL databases.
    """
    if "postgresql" not in connection.settings_dict["ENGINE"]:
        return
    for table_name in table_names:
        for sql in enable_rls_for_table_sql(table_name):
            schema_editor.execute(sql)


def enable_rls_on_all_models(apps, schema_editor):
    """
    Enables RLS for all tables in the database by applying RLS policies for each table.
    """
    # Gather all tables with a ContentType
    content_types = ContentType.objects.all()
    tables_to_apply = [
        content_type.model_class()._meta.db_table
        for content_type in content_types
        if content_type.model_class() is not None
    ]
    # Apply RLS to all gathered tables
    enable_rls_on_tables(schema_editor, tables_to_apply)


def apply_rls_on_additional_tables(table_names):
    """
    Returns a function that can be used to apply RLS on specified tables in a migration.
    """

    def apply_rls(apps, schema_editor):
        enable_rls_on_tables(schema_editor, table_names)

    return apply_rls
