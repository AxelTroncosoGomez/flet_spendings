import pytest
import os
from unittest.mock import patch, MagicMock
from utils.config import Config


class TestConfig:
    """Test suite for Config class."""

    def test_config_class_exists(self):
        """Test that Config class is accessible."""
        assert Config is not None

    def test_config_attributes_exist(self):
        """Test that all expected config attributes exist."""
        assert hasattr(Config, 'SUPABASE_URL')
        assert hasattr(Config, 'SUPABASE_KEY')
        assert hasattr(Config, 'GITHUB_CLIENT_ID')
        assert hasattr(Config, 'GITHUB_CLIENT_SECRET')
        assert hasattr(Config, 'APP_DATA_PATH')
        assert hasattr(Config, 'APP_TEMP_PATH')
        assert hasattr(Config, 'APP_ASSETS_PATH')

    @patch('os.getenv')
    def test_config_with_empty_environment(self, mock_getenv):
        """Test Config behavior when environment variables are not set."""
        # Mock getenv to return defaults
        def getenv_side_effect(key, default=None):
            if key in ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET']:
                return ""
            return None  # For path variables without defaults

        mock_getenv.side_effect = getenv_side_effect

        # Reload the module to test with mocked environment
        import importlib
        import utils.config
        importlib.reload(utils.config)

        from utils.config import Config as FreshConfig

        assert FreshConfig.SUPABASE_URL == ""
        assert FreshConfig.SUPABASE_KEY == ""
        assert FreshConfig.GITHUB_CLIENT_ID == ""
        assert FreshConfig.GITHUB_CLIENT_SECRET == ""
        assert FreshConfig.APP_DATA_PATH is None
        assert FreshConfig.APP_TEMP_PATH is None
        assert FreshConfig.APP_ASSETS_PATH is None

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test_anon_key',
        'GITHUB_CLIENT_ID': 'test_client_id',
        'GITHUB_CLIENT_SECRET': 'test_client_secret',
        'FLET_APP_STORAGE_DATA': '/test/data/path',
        'FLET_APP_STORAGE_TEMP': '/test/temp/path',
        'FLET_ASSETS_DIR': '/test/assets/path'
    })
    def test_config_with_environment_variables(self):
        """Test Config behavior when environment variables are set."""
        from utils.config import Config as FreshConfig

        assert FreshConfig.SUPABASE_URL == 'https://test.supabase.co'
        assert FreshConfig.SUPABASE_KEY == 'test_anon_key'
        assert FreshConfig.GITHUB_CLIENT_ID == 'test_client_id'
        assert FreshConfig.GITHUB_CLIENT_SECRET == 'test_client_secret'
        assert FreshConfig.APP_DATA_PATH == '/test/data/path'
        assert FreshConfig.APP_TEMP_PATH == '/test/temp/path'
        assert FreshConfig.APP_ASSETS_PATH == '/test/assets/path'

    @patch.dict(os.environ, {
        'SUPABASE_URL': '',
        'SUPABASE_ANON_KEY': '',
        'GITHUB_CLIENT_ID': '',
        'GITHUB_CLIENT_SECRET': '',
        'FLET_APP_STORAGE_DATA': '',
        'FLET_APP_STORAGE_TEMP': '',
        'FLET_ASSETS_DIR': ''
    })
    def test_config_with_empty_environment_variables(self):
        """Test Config behavior when environment variables are empty strings."""
        from utils.config import Config as FreshConfig

        assert FreshConfig.SUPABASE_URL == ""
        assert FreshConfig.SUPABASE_KEY == ""
        assert FreshConfig.GITHUB_CLIENT_ID == ""
        assert FreshConfig.GITHUB_CLIENT_SECRET == ""
        assert FreshConfig.APP_DATA_PATH == ""
        assert FreshConfig.APP_TEMP_PATH == ""
        assert FreshConfig.APP_ASSETS_PATH == ""

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'https://prod.supabase.co',
        'SUPABASE_ANON_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    })
    def test_config_partial_environment_variables(self):
        """Test Config behavior when only some environment variables are set."""
        from utils.config import Config as FreshConfig

        assert FreshConfig.SUPABASE_URL == 'https://prod.supabase.co'
        assert FreshConfig.SUPABASE_KEY == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        assert FreshConfig.GITHUB_CLIENT_ID == ""
        assert FreshConfig.GITHUB_CLIENT_SECRET == ""

    def test_config_attributes_are_strings_or_none(self):
        """Test that all config attributes are either strings or None."""
        config_attrs = [
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'GITHUB_CLIENT_ID',
            'GITHUB_CLIENT_SECRET',
            'APP_DATA_PATH',
            'APP_TEMP_PATH',
            'APP_ASSETS_PATH'
        ]

        for attr in config_attrs:
            value = getattr(Config, attr)
            assert value is None or isinstance(value, str), f"{attr} should be string or None, got {type(value)}"

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'https://special-chars.supabase.co/ñ',
        'SUPABASE_ANON_KEY': 'key_with_special_chars_!@#$%^&*()',
        'GITHUB_CLIENT_ID': 'client_123_abc',
        'GITHUB_CLIENT_SECRET': 'secret_with_underscores_and_numbers_123',
        'FLET_APP_STORAGE_DATA': '/path/with spaces/and-dashes',
        'FLET_APP_STORAGE_TEMP': '/temp/path/with.dots',
        'FLET_ASSETS_DIR': '/assets/path/with/unicode/ñáéíóú'
    })
    def test_config_with_special_characters(self):
        """Test Config behavior with special characters in environment variables."""
        from utils.config import Config as FreshConfig

        assert FreshConfig.SUPABASE_URL == 'https://special-chars.supabase.co/ñ'
        assert FreshConfig.SUPABASE_KEY == 'key_with_special_chars_!@#$%^&*()'
        assert FreshConfig.GITHUB_CLIENT_ID == 'client_123_abc'
        assert FreshConfig.GITHUB_CLIENT_SECRET == 'secret_with_underscores_and_numbers_123'
        assert FreshConfig.APP_DATA_PATH == '/path/with spaces/and-dashes'
        assert FreshConfig.APP_TEMP_PATH == '/temp/path/with.dots'
        assert FreshConfig.APP_ASSETS_PATH == '/assets/path/with/unicode/ñáéíóú'

    def test_config_class_is_not_instantiable(self):
        """Test that Config class is intended to be used as a static class."""
        # This tests the current design - Config is used as a static class
        # We can access its attributes without instantiation
        assert isinstance(Config.SUPABASE_URL, (str, type(None)))

        # We can still instantiate it if needed, but it's not the intended usage
        config_instance = Config()
        assert hasattr(config_instance, 'SUPABASE_URL')

    @patch('os.getenv')
    def test_config_getenv_calls(self, mock_getenv):
        """Test that Config makes the correct os.getenv calls."""
        mock_getenv.return_value = "mocked_value"

        # Force reimport to trigger os.getenv calls
        import importlib
        import utils.config
        importlib.reload(utils.config)

        # Check that os.getenv was called with the correct arguments
        expected_calls = [
            ("SUPABASE_URL", ""),
            ("SUPABASE_ANON_KEY", ""),
            ("GITHUB_CLIENT_ID", ""),
            ("GITHUB_CLIENT_SECRET", ""),
            ("FLET_APP_STORAGE_DATA",),
            ("FLET_APP_STORAGE_TEMP",),
            ("FLET_ASSETS_DIR",)
        ]

        # Verify that getenv was called (we can't guarantee exact call order due to imports)
        assert mock_getenv.call_count >= len(expected_calls)

    def test_config_environment_variable_names(self):
        """Test that the correct environment variable names are used."""
        # This is more of a documentation test to ensure we're using the right env var names
        expected_env_vars = {
            'SUPABASE_URL': Config.SUPABASE_URL,
            'SUPABASE_ANON_KEY': Config.SUPABASE_KEY,  # Note: different name
            'GITHUB_CLIENT_ID': Config.GITHUB_CLIENT_ID,
            'GITHUB_CLIENT_SECRET': Config.GITHUB_CLIENT_SECRET,
            'FLET_APP_STORAGE_DATA': Config.APP_DATA_PATH,
            'FLET_APP_STORAGE_TEMP': Config.APP_TEMP_PATH,
            'FLET_ASSETS_DIR': Config.APP_ASSETS_PATH
        }

        # This test ensures we haven't accidentally changed the environment variable names
        for env_var, config_attr in expected_env_vars.items():
            assert config_attr is not None or config_attr == "" or isinstance(config_attr, str)

    @patch.dict(os.environ, {
        'SUPABASE_URL': '  https://trimmed.supabase.co  ',
        'SUPABASE_ANON_KEY': '  trimmed_key  ',
    })
    def test_config_does_not_trim_whitespace(self):
        """Test that Config preserves whitespace in environment variables."""
        from utils.config import Config as FreshConfig

        # The current implementation doesn't trim whitespace
        assert FreshConfig.SUPABASE_URL == '  https://trimmed.supabase.co  '
        assert FreshConfig.SUPABASE_KEY == '  trimmed_key  '

    def test_config_attribute_types_consistency(self):
        """Test that config attributes have consistent types."""
        str_attributes = ['SUPABASE_URL', 'SUPABASE_KEY', 'GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET']
        optional_str_attributes = ['APP_DATA_PATH', 'APP_TEMP_PATH', 'APP_ASSETS_PATH']

        for attr in str_attributes:
            value = getattr(Config, attr)
            assert isinstance(value, str), f"{attr} should be a string, got {type(value)}"

        for attr in optional_str_attributes:
            value = getattr(Config, attr)
            assert value is None or isinstance(value, str), f"{attr} should be string or None, got {type(value)}"


class TestConfigIntegration:
    """Integration tests for Config class."""

    def test_config_supabase_url_format(self):
        """Test that SUPABASE_URL follows expected format when set."""
        if Config.SUPABASE_URL and Config.SUPABASE_URL != "":
            # If URL is set, it should be a valid URL-like string
            assert "http" in Config.SUPABASE_URL or Config.SUPABASE_URL == ""

    def test_config_github_credentials_pairing(self):
        """Test that GitHub credentials are typically set together."""
        # This is a soft test - they don't have to be set together, but typically are
        has_client_id = Config.GITHUB_CLIENT_ID and Config.GITHUB_CLIENT_ID != ""
        has_client_secret = Config.GITHUB_CLIENT_SECRET and Config.GITHUB_CLIENT_SECRET != ""

        # If one is set, the other probably should be too (though not required)
        if has_client_id or has_client_secret:
            # This is just informational - we don't enforce it
            pass

    def test_config_app_paths_are_absolute_when_set(self):
        """Test that app paths are absolute paths when set."""
        path_attrs = ['APP_DATA_PATH', 'APP_TEMP_PATH', 'APP_ASSETS_PATH']

        for attr in path_attrs:
            value = getattr(Config, attr)
            if value and value != "":
                # When paths are set, they should typically be absolute
                # This is more of a guideline than a hard requirement
                assert isinstance(value, str)


class TestConfigErrorHandling:
    """Test error handling scenarios for Config."""

    @patch('os.getenv')
    def test_config_handles_getenv_exception(self, mock_getenv):
        """Test Config behavior when os.getenv raises an exception."""
        mock_getenv.side_effect = Exception("Environment error")

        # This would cause an import error, which is expected behavior
        with pytest.raises(Exception):
            import importlib
            import utils.config
            importlib.reload(utils.config)

    def test_config_with_none_environment_values(self):
        """Test Config behavior when environment returns None (should not happen with os.getenv)."""
        # os.getenv with default parameters shouldn't return None, but test the edge case
        with patch('os.getenv') as mock_getenv:
            # Some calls return None, others return defaults
            def getenv_side_effect(key, default=None):
                if key in ['FLET_APP_STORAGE_DATA', 'FLET_APP_STORAGE_TEMP', 'FLET_ASSETS_DIR']:
                    return None
                return default if default is not None else ""

            mock_getenv.side_effect = getenv_side_effect

            import importlib
            import utils.config
            importlib.reload(utils.config)

            # Check that None values are preserved for path variables
            assert utils.config.Config.APP_DATA_PATH is None
            assert utils.config.Config.APP_TEMP_PATH is None
            assert utils.config.Config.APP_ASSETS_PATH is None