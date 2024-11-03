from unittest import mock

from main.migrations_helpers import enable_rls_for_table_sql, enable_rls_on_all_models


class TestMigrationsHelpers:
    @mock.patch("main.migrations_helpers.connection")
    @mock.patch("main.migrations_helpers.ContentType")
    def test_enable_rls_on_all_models_with_postgresql(
        self, mock_content_type, mock_connection
    ):
        mock_connection.settings_dict = {"ENGINE": "django.db.backends.postgresql"}
        # Mock ContentType.objects.all() to return a list of mock content types
        mock_model = mock.Mock(_meta=mock.Mock(db_table="test_table"))
        mock_content_type.objects.all.return_value = [
            mock.Mock(model_class=lambda: mock_model)
        ]
        # Mock the schema_editor.execute method to track SQL execution
        mock_schema_editor = mock.Mock()
        enable_rls_on_all_models(apps=None, schema_editor=mock_schema_editor)
        # Verify the SQL commands generated for "test_table"
        expected_sql_commands = enable_rls_for_table_sql("test_table")
        for sql_command in expected_sql_commands:
            mock_schema_editor.execute.assert_any_call(sql_command)
        # Ensure the SQL was executed the correct number of times
        assert mock_schema_editor.execute.call_count == len(expected_sql_commands)
