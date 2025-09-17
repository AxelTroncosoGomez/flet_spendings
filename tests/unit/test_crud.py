import pytest
import os
import sqlite3
import uuid
import tempfile
import shutil
from unittest.mock import patch, MagicMock, call
from datetime import datetime

from services.crud import LocalSpendingsDatabase


class TestLocalSpendingsDatabase:
    """Test suite for LocalSpendingsDatabase class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test databases."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def mock_env_paths(self, temp_dir):
        """Mock environment paths for testing."""
        with patch.dict(os.environ, {
            'FLET_APP_STORAGE_DATA': temp_dir,
            'FLET_APP_STORAGE_TEMP': temp_dir
        }):
            yield temp_dir

    @pytest.fixture
    def database(self, mock_env_paths):
        """Create a LocalSpendingsDatabase instance for testing."""
        db_name = "test_spendings.db"
        user_id = "test_user_123"
        return LocalSpendingsDatabase(db_name, user_id)

    @pytest.fixture
    def connected_database(self, database):
        """Create and connect a database for testing."""
        database.create_or_open()
        yield database
        if database.conn:
            database.close()

    def test_initialization(self, mock_env_paths):
        """Test LocalSpendingsDatabase initialization."""
        db_name = "test.db"
        user_id = "user123"

        db = LocalSpendingsDatabase(db_name, user_id)

        assert db.db == db_name
        assert db.user == user_id
        assert db.conn is None
        assert db.db_path == os.path.join(mock_env_paths, db_name)
        assert db._database_name == "spendings"

    def test_initialization_with_none_app_data_path(self):
        """Test initialization when APP_DATA_PATH is None."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.getenv', return_value=None):
                db_name = "test.db"
                user_id = "user123"

                with pytest.raises(TypeError):  # os.path.join will fail with None
                    LocalSpendingsDatabase(db_name, user_id)

    def test_connect(self, database, mock_env_paths):
        """Test database connection."""
        database.connect()

        assert database.conn is not None
        assert database.pencil is not None
        assert isinstance(database.conn, sqlite3.Connection)

        database.close()

    def test_create_or_open_creates_table(self, database):
        """Test that create_or_open creates the spendings table."""
        database.create_or_open()

        # Check that table exists
        cursor = database.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spendings'")
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == "spendings"

        database.close()

    def test_create_or_open_table_schema(self, database):
        """Test that the created table has the correct schema."""
        database.create_or_open()

        cursor = database.conn.cursor()
        cursor.execute("PRAGMA table_info(spendings)")
        columns = cursor.fetchall()

        expected_columns = [
            ('item_id', 'TEXT', 0, None, 1),  # PRIMARY KEY
            ('user_id', 'TEXT', 1, None, 0),  # NOT NULL
            ('date', 'TEXT', 1, None, 0),     # NOT NULL
            ('store', 'TEXT', 1, None, 0),   # NOT NULL
            ('product', 'TEXT', 1, None, 0), # NOT NULL
            ('amount', 'INTEGER', 1, None, 0), # NOT NULL
            ('price', 'FLOAT', 1, None, 0)   # NOT NULL
        ]

        assert len(columns) == len(expected_columns)
        for i, (name, type_, notnull, default, pk) in enumerate(expected_columns):
            assert columns[i][1] == name
            assert columns[i][2] == type_
            assert columns[i][3] == notnull

        database.close()

    def test_create_or_open_already_connected(self, connected_database):
        """Test create_or_open when database is already connected."""
        # Should not raise an exception
        connected_database.create_or_open()
        assert connected_database.conn is not None

    def test_insert_single_row(self, connected_database):
        """Test inserting a single row."""
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)

        connected_database.insert(row)

        # Verify insertion
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT * FROM spendings WHERE item_id = ?", (item_id,))
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == item_id
        assert result[1] == "test_user_123"
        assert result[2] == "01/01/2024"
        assert result[3] == "Test Store"
        assert result[4] == "Test Product"
        assert result[5] == 1
        assert result[6] == 10.50

    def test_insert_multiple_rows(self, connected_database):
        """Test inserting multiple rows."""
        rows = [
            (str(uuid.uuid4()), "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50),
            (str(uuid.uuid4()), "test_user_123", "02/01/2024", "Store 2", "Product 2", 2, 20.75)
        ]

        for row in rows:
            connected_database.insert(row)

        # Verify insertions
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM spendings WHERE user_id = ?", ("test_user_123",))
        count = cursor.fetchone()[0]

        assert count == 2

    def test_select_all_data_with_id(self, connected_database):
        """Test selecting all data including IDs."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Select all data
        results = connected_database.select_all_data(exclude_id=False)

        assert len(results) == 1
        assert results[0][0] == item_id  # item_id should be included
        assert results[0][1] == "test_user_123"

    def test_select_all_data_exclude_id(self, connected_database):
        """Test selecting all data excluding IDs."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Select all data excluding ID
        results = connected_database.select_all_data(exclude_id=True)

        assert len(results) == 1
        assert results[0][0] == "test_user_123"  # user_id should be first (item_id excluded)
        assert len(results[0]) == 6  # Should have 6 columns instead of 7

    def test_select_all_data_user_filtering(self, connected_database):
        """Test that select_all_data only returns data for the current user."""
        # Insert data for different users
        item_id1 = str(uuid.uuid4())
        item_id2 = str(uuid.uuid4())
        row1 = (item_id1, "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50)
        row2 = (item_id2, "other_user", "01/01/2024", "Store 2", "Product 2", 1, 15.75)

        connected_database.insert(row1)
        connected_database.insert(row2)

        # Should only return data for test_user_123
        results = connected_database.select_all_data()
        assert len(results) == 1
        assert results[0][1] == "test_user_123"

    def test_select_data_from_date_default(self, connected_database):
        """Test selecting data from today's date (default)."""
        today = datetime.now().date().strftime("%d/%m/%Y")
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", today, "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        results = connected_database.select_data_from_date()

        assert len(results) == 1
        assert results[0][2] == today

    def test_select_data_from_date_specific(self, connected_database):
        """Test selecting data from a specific date."""
        target_date = "15/06/2024"
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", target_date, "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Insert data for different date
        other_date = "16/06/2024"
        item_id2 = str(uuid.uuid4())
        row2 = (item_id2, "test_user_123", other_date, "Other Store", "Other Product", 1, 20.50)
        connected_database.insert(row2)

        results = connected_database.select_data_from_date(target_date)

        assert len(results) == 1
        assert results[0][2] == target_date

    def test_select_data_from_date_exclude_id(self, connected_database):
        """Test selecting data from date excluding ID columns."""
        target_date = "15/06/2024"
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", target_date, "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        results = connected_database.select_data_from_date(target_date, exclude_id=True)

        assert len(results) == 1
        assert len(results[0]) == 5  # Should exclude item_id and user_id (first 2 columns)
        assert results[0][0] == target_date  # Date should be first after excluding IDs

    def test_delete_row_by_id(self, connected_database):
        """Test deleting a row by ID."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Verify insertion
        results = connected_database.select_all_data()
        assert len(results) == 1

        # Delete the row
        connected_database.delete_row_by_id(item_id)

        # Verify deletion
        results = connected_database.select_all_data()
        assert len(results) == 0

    def test_delete_row_by_id_user_scoped(self, connected_database):
        """Test that delete_row_by_id only deletes rows for the current user."""
        # Insert data for different users with same item_id
        item_id = str(uuid.uuid4())
        row1 = (item_id, "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50)
        row2 = (item_id, "other_user", "01/01/2024", "Store 2", "Product 2", 1, 15.75)

        connected_database.insert(row1)
        connected_database.insert(row2)

        # Delete should only affect the current user's row
        connected_database.delete_row_by_id(item_id)

        # Check that only one row remains (the other user's row)
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT * FROM spendings")
        results = cursor.fetchall()
        assert len(results) == 1
        assert results[0][1] == "other_user"

    def test_delete_rows_by_ids(self, connected_database):
        """Test deleting multiple rows by IDs."""
        # Insert test data
        item_ids = [str(uuid.uuid4()) for _ in range(3)]
        rows = [
            (item_ids[0], "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50),
            (item_ids[1], "test_user_123", "02/01/2024", "Store 2", "Product 2", 1, 20.50),
            (item_ids[2], "test_user_123", "03/01/2024", "Store 3", "Product 3", 1, 30.50)
        ]

        for row in rows:
            connected_database.insert(row)

        # Delete first two rows
        connected_database.delete_rows_by_ids(item_ids[:2])

        # Verify only one row remains
        results = connected_database.select_all_data()
        assert len(results) == 1
        assert results[0][0] == item_ids[2]

    def test_update_row(self, connected_database):
        """Test updating a row."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Old Store", "Old Product", 1, 10.50)
        connected_database.insert(row)

        # Update the row
        new_values = ("02/01/2024", "New Store", "New Product", 2, 25.75)
        connected_database.update(item_id, new_values)

        # Verify update
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT * FROM spendings WHERE item_id = ?", (item_id,))
        result = cursor.fetchone()

        assert result[2] == "02/01/2024"  # date
        assert result[3] == "New Store"   # store
        assert result[4] == "New Product" # product
        assert result[5] == 2             # amount
        assert result[6] == 25.75         # price

    def test_update_row_user_scoped(self, connected_database):
        """Test that update only affects rows for the current user."""
        # Insert data for different users with same item_id
        item_id = str(uuid.uuid4())
        row1 = (item_id, "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50)
        row2 = (item_id, "other_user", "01/01/2024", "Store 2", "Product 2", 1, 15.75)

        connected_database.insert(row1)
        connected_database.insert(row2)

        # Update should only affect the current user's row
        new_values = ("02/01/2024", "Updated Store", "Updated Product", 3, 35.25)
        connected_database.update(item_id, new_values)

        # Check that only the current user's row was updated
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT * FROM spendings WHERE user_id = ?", ("test_user_123",))
        result = cursor.fetchone()
        assert result[3] == "Updated Store"

        cursor.execute("SELECT * FROM spendings WHERE user_id = ?", ("other_user",))
        result = cursor.fetchone()
        assert result[3] == "Store 2"  # Should remain unchanged

    def test_get_id_from_row(self, connected_database):
        """Test getting item ID from row data."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row_data = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row_data)

        # Get ID from row (excluding item_id and user_id from search)
        search_row = ("01/01/2024", "Test Store", "Test Product", 1, 10.50, "test_user_123")
        found_id = connected_database.get_id_from_row(search_row)

        assert found_id == item_id

    def test_get_id_from_row_not_found(self, connected_database):
        """Test getting item ID when row doesn't exist."""
        search_row = ("01/01/2024", "Nonexistent Store", "Nonexistent Product", 1, 10.50, "test_user_123")
        found_id = connected_database.get_id_from_row(search_row)

        assert found_id is None

    def test_custom_query_execution(self, connected_database):
        """Test custom query execution."""
        # Insert test data first
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Execute custom update query
        query = f"UPDATE spendings SET price = 99.99 WHERE item_id = '{item_id}'"
        connected_database.custom_query_execution(query)

        # Verify the custom query worked
        cursor = connected_database.conn.cursor()
        cursor.execute("SELECT price FROM spendings WHERE item_id = ?", (item_id,))
        result = cursor.fetchone()
        assert result[0] == 99.99

    def test_custom_fetch_execution(self, connected_database):
        """Test custom fetch execution."""
        # Insert test data
        item_ids = [str(uuid.uuid4()) for _ in range(2)]
        rows = [
            (item_ids[0], "test_user_123", "01/01/2024", "Store 1", "Product 1", 1, 10.50),
            (item_ids[1], "test_user_123", "02/01/2024", "Store 2", "Product 2", 2, 20.50)
        ]

        for row in rows:
            connected_database.insert(row)

        # Execute custom fetch query
        query = "SELECT store, product FROM spendings WHERE user_id = 'test_user_123' ORDER BY date"
        results = connected_database.custom_fetch_execution(query)

        assert len(results) == 2
        assert results[0] == ("Store 1", "Product 1")
        assert results[1] == ("Store 2", "Product 2")

    def test_close_connection(self, database):
        """Test closing database connection."""
        database.create_or_open()
        assert database.conn is not None

        database.close()
        # Connection should be closed but still exist as object
        assert database.conn is not None

        # Try to use closed connection (should fail)
        with pytest.raises(sqlite3.ProgrammingError):
            database.conn.execute("SELECT 1")

    def test_close_connection_when_none(self, database):
        """Test closing connection when it's None."""
        assert database.conn is None
        # Should not raise an exception
        database.close()

    @patch('services.crud.logger')
    def test_private_reset_method(self, mock_logger, connected_database):
        """Test the private __reset method."""
        # Insert test data
        item_id = str(uuid.uuid4())
        row = (item_id, "test_user_123", "01/01/2024", "Test Store", "Test Product", 1, 10.50)
        connected_database.insert(row)

        # Verify data exists
        results = connected_database.select_all_data()
        assert len(results) == 1

        # Call private reset method
        connected_database._LocalSpendingsDatabase__reset()

        # Verify data is deleted
        results = connected_database.select_all_data()
        assert len(results) == 0

    @patch('services.crud.logger')
    def test_private_reset_method_error_handling(self, mock_logger, database):
        """Test __reset method error handling when not connected."""
        # Try to reset without connection
        database._LocalSpendingsDatabase__reset()

        # Should log debug message about failure
        mock_logger.debug.assert_called_once()
        assert "Failed to reset database" in mock_logger.debug.call_args[0][0]


class TestLocalSpendingsDatabaseEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test databases."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_database_with_special_characters_in_name(self, temp_dir):
        """Test database with special characters in name."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db_name = "test-db_with.special-chars.db"
            user_id = "user_with_special_chars_123"
            db = LocalSpendingsDatabase(db_name, user_id)
            db.create_or_open()

            assert db.conn is not None
            db.close()

    def test_database_with_unicode_user_id(self, temp_dir):
        """Test database with unicode characters in user ID."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db_name = "unicode_test.db"
            user_id = "user_ñáéíóú_测试"
            db = LocalSpendingsDatabase(db_name, user_id)
            db.create_or_open()

            # Insert data with unicode user ID
            item_id = str(uuid.uuid4())
            row = (item_id, user_id, "01/01/2024", "Test Store", "Test Product", 1, 10.50)
            db.insert(row)

            results = db.select_all_data()
            assert len(results) == 1
            assert results[0][1] == user_id

            db.close()

    def test_insert_with_unicode_data(self, temp_dir):
        """Test inserting data with unicode characters."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db = LocalSpendingsDatabase("unicode.db", "test_user")
            db.create_or_open()

            item_id = str(uuid.uuid4())
            row = (item_id, "test_user", "01/01/2024", "Tienda Española", "Producto ñ", 1, 10.50)
            db.insert(row)

            results = db.select_all_data()
            assert len(results) == 1
            assert results[0][3] == "Tienda Española"
            assert results[0][4] == "Producto ñ"

            db.close()

    def test_very_large_data_insert(self, temp_dir):
        """Test inserting very large string data."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db = LocalSpendingsDatabase("large_data.db", "test_user")
            db.create_or_open()

            large_text = "X" * 10000  # 10KB string
            item_id = str(uuid.uuid4())
            row = (item_id, "test_user", "01/01/2024", large_text, "Product", 1, 10.50)
            db.insert(row)

            results = db.select_all_data()
            assert len(results) == 1
            assert results[0][3] == large_text

            db.close()

    def test_concurrent_database_access(self, temp_dir):
        """Test multiple database instances accessing the same file."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db1 = LocalSpendingsDatabase("shared.db", "user1")
            db2 = LocalSpendingsDatabase("shared.db", "user2")

            db1.create_or_open()
            db2.create_or_open()

            # Insert data from both instances
            item_id1 = str(uuid.uuid4())
            item_id2 = str(uuid.uuid4())
            db1.insert((item_id1, "user1", "01/01/2024", "Store 1", "Product 1", 1, 10.50))
            db2.insert((item_id2, "user2", "01/01/2024", "Store 2", "Product 2", 1, 20.50))

            # Each should only see their own data
            results1 = db1.select_all_data()
            results2 = db2.select_all_data()

            assert len(results1) == 1
            assert len(results2) == 1
            assert results1[0][1] == "user1"
            assert results2[0][1] == "user2"

            db1.close()
            db2.close()

    @patch('services.crud.logger')
    def test_update_error_handling(self, mock_logger, temp_dir):
        """Test update method error handling."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db = LocalSpendingsDatabase("error_test.db", "test_user")
            db.create_or_open()

            # Try to update non-existent item (should not raise but might log)
            new_values = ("02/01/2024", "Store", "Product", 1, 10.50)
            db.update("nonexistent_id", new_values)

            # Close connection and try to update (should cause error and log)
            db.close()
            db.update("some_id", new_values)

            # Should have logged an error
            assert mock_logger.debug.call_count > 0

    def test_empty_string_values(self, temp_dir):
        """Test handling of empty string values."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db = LocalSpendingsDatabase("empty_strings.db", "test_user")
            db.create_or_open()

            item_id = str(uuid.uuid4())
            row = (item_id, "test_user", "", "", "", 0, 0.0)
            db.insert(row)

            results = db.select_all_data()
            assert len(results) == 1
            assert results[0][2] == ""  # date
            assert results[0][3] == ""  # store
            assert results[0][4] == ""  # product

            db.close()

    def test_zero_and_negative_values(self, temp_dir):
        """Test handling of zero and negative numeric values."""
        with patch.dict(os.environ, {'FLET_APP_STORAGE_DATA': temp_dir}):
            db = LocalSpendingsDatabase("numeric_edge.db", "test_user")
            db.create_or_open()

            # Test with zero values
            item_id1 = str(uuid.uuid4())
            row1 = (item_id1, "test_user", "01/01/2024", "Store", "Product", 0, 0.0)
            db.insert(row1)

            # Test with negative values
            item_id2 = str(uuid.uuid4())
            row2 = (item_id2, "test_user", "01/01/2024", "Store", "Product", -1, -10.50)
            db.insert(row2)

            results = db.select_all_data()
            assert len(results) == 2

            # Find and verify the specific rows
            zero_row = next(r for r in results if r[0] == item_id1)
            negative_row = next(r for r in results if r[0] == item_id2)

            assert zero_row[5] == 0
            assert zero_row[6] == 0.0
            assert negative_row[5] == -1
            assert negative_row[6] == -10.50

            db.close()