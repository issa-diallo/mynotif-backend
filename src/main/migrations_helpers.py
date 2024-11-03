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


def enable_rls_on_all_models(apps, schema_editor):
    """
    Enables RLS for all tables in the database by applying RLS policies for each table.
    Only applies to PostgreSQL databases.
    """
    # Check if the database engine is PostgreSQL
    if "postgresql" not in connection.settings_dict["ENGINE"]:
        return
    content_types = ContentType.objects.all()
    for content_type in content_types:
        model = content_type.model_class()
        if model is not None:
            table_name = model._meta.db_table
            # Apply RLS SQL commands for each table
            for sql in enable_rls_for_table_sql(table_name):
                schema_editor.execute(sql)
