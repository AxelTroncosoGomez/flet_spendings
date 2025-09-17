import pytest
from exceptions import (
    AppError,
    GenericException,
    WrongCredentialsException,
    WrongPasswordException,
    UserAlreadyExistsException,
    EmailNotConfirmedException,
    UserNotAllowedException,
    SupabaseApiException,
    PasswordNotEqualException,
    InputNotFilledException,
    InvalidInputException,
    EmailNotValidException,
    SupabaseRLSViolationException,
    SupabaseDuplicateKeyConstraintException,
    SupabaseNullValueInsertionException,
    InvalidCredentialsException,
    UserNotLoggedException
)


class TestAppError:
    """Test suite for AppError exception."""

    def test_app_error_initialization_with_complete_error_dict(self):
        """Test AppError initialization with complete error dictionary."""
        error_dict = {
            "message": "Test error message",
            "code": "TEST_001",
            "hint": "This is a test hint",
            "details": "Detailed error information"
        }

        app_error = AppError(error_dict)

        assert app_error.message == "Test error message"
        assert app_error.code == "TEST_001"
        assert app_error.hint == "This is a test hint"
        assert app_error.details == "Detailed error information"
        # Note: str() returns the raw error dict due to implementation detail
        # This tests the actual behavior, not necessarily the intended behavior
        assert str(app_error) == str(error_dict)

    def test_app_error_initialization_with_partial_error_dict(self):
        """Test AppError initialization with partial error dictionary."""
        error_dict = {
            "message": "Test error message",
            "code": "TEST_002"
        }

        app_error = AppError(error_dict)

        assert app_error.message == "Test error message"
        assert app_error.code == "TEST_002"
        assert app_error.hint is None
        assert app_error.details is None

    def test_app_error_initialization_with_empty_dict(self):
        """Test AppError initialization with empty dictionary."""
        error_dict = {}

        app_error = AppError(error_dict)

        assert app_error.message is None
        assert app_error.code is None
        assert app_error.hint is None
        assert app_error.details is None

    def test_app_error_repr_with_all_fields(self):
        """Test AppError string representation with all fields."""
        error_dict = {
            "message": "Test error message",
            "code": "TEST_003",
            "hint": "This is a test hint",
            "details": "Detailed error information"
        }

        app_error = AppError(error_dict)
        expected_repr = "Error TEST_003:\nMessage: Test error message\nHint: This is a test hint\nDetails: Detailed error information"

        assert repr(app_error) == expected_repr

    def test_app_error_repr_with_message_only(self):
        """Test AppError string representation with message only."""
        error_dict = {
            "message": "Test error message"
        }

        app_error = AppError(error_dict)
        expected_repr = "\nMessage: Test error message"

        assert repr(app_error) == expected_repr

    def test_app_error_repr_with_code_only(self):
        """Test AppError string representation with code only."""
        error_dict = {
            "code": "TEST_004"
        }

        app_error = AppError(error_dict)
        expected_repr = "Error TEST_004:"

        assert repr(app_error) == expected_repr

    def test_app_error_repr_empty_error(self):
        """Test AppError string representation with empty error."""
        error_dict = {}

        app_error = AppError(error_dict)

        assert repr(app_error) == "Empty error"

    def test_app_error_json_method(self):
        """Test AppError json method returns original dict."""
        error_dict = {
            "message": "Test error message",
            "code": "TEST_005",
            "extra_field": "extra_value"
        }

        app_error = AppError(error_dict)

        assert app_error.json() == error_dict

    def test_app_error_inheritance(self):
        """Test AppError inherits from Exception."""
        error_dict = {"message": "Test"}
        app_error = AppError(error_dict)

        assert isinstance(app_error, Exception)

    def test_app_error_with_special_characters(self):
        """Test AppError with special characters in fields."""
        error_dict = {
            "message": "Error with 'quotes' and \"double quotes\"",
            "code": "SPECIAL_001",
            "hint": "Hint with\nnewline",
            "details": "Details with\ttab"
        }

        app_error = AppError(error_dict)

        assert "Error with 'quotes' and \"double quotes\"" in repr(app_error)
        assert "SPECIAL_001" in repr(app_error)
        assert "Hint with\nnewline" in repr(app_error)
        assert "Details with\ttab" in repr(app_error)

    def test_app_error_with_none_values(self):
        """Test AppError with None values in dictionary."""
        error_dict = {
            "message": None,
            "code": None,
            "hint": None,
            "details": None
        }

        app_error = AppError(error_dict)

        assert app_error.message is None
        assert app_error.code is None
        assert app_error.hint is None
        assert app_error.details is None
        assert repr(app_error) == "Empty error"


class TestSimpleExceptions:
    """Test suite for simple custom exceptions."""

    def test_generic_exception(self):
        """Test GenericException instantiation."""
        exception = GenericException("Test message")
        assert isinstance(exception, Exception)
        assert str(exception) == "Test message"

    def test_wrong_credentials_exception(self):
        """Test WrongCredentialsException instantiation."""
        exception = WrongCredentialsException("Invalid credentials")
        assert isinstance(exception, Exception)
        assert str(exception) == "Invalid credentials"

    def test_wrong_password_exception(self):
        """Test WrongPasswordException instantiation."""
        exception = WrongPasswordException("Incorrect password")
        assert isinstance(exception, Exception)
        assert str(exception) == "Incorrect password"

    def test_user_already_exists_exception(self):
        """Test UserAlreadyExistsException instantiation."""
        exception = UserAlreadyExistsException("User exists")
        assert isinstance(exception, Exception)
        assert str(exception) == "User exists"

    def test_email_not_confirmed_exception(self):
        """Test EmailNotConfirmedException instantiation."""
        exception = EmailNotConfirmedException("Email not confirmed")
        assert isinstance(exception, Exception)
        assert str(exception) == "Email not confirmed"

    def test_user_not_allowed_exception(self):
        """Test UserNotAllowedException instantiation."""
        exception = UserNotAllowedException("User not allowed")
        assert isinstance(exception, Exception)
        assert str(exception) == "User not allowed"

    def test_supabase_api_exception(self):
        """Test SupabaseApiException instantiation."""
        exception = SupabaseApiException("Supabase API error")
        assert isinstance(exception, Exception)
        assert str(exception) == "Supabase API error"

    def test_password_not_equal_exception(self):
        """Test PasswordNotEqualException instantiation."""
        exception = PasswordNotEqualException("Passwords do not match")
        assert isinstance(exception, Exception)
        assert str(exception) == "Passwords do not match"

    def test_input_not_filled_exception(self):
        """Test InputNotFilledException instantiation."""
        exception = InputNotFilledException("Required field not filled")
        assert isinstance(exception, Exception)
        assert str(exception) == "Required field not filled"

    def test_invalid_input_exception(self):
        """Test InvalidInputException instantiation."""
        exception = InvalidInputException("Invalid input format")
        assert isinstance(exception, Exception)
        assert str(exception) == "Invalid input format"

    def test_email_not_valid_exception(self):
        """Test EmailNotValidException instantiation."""
        exception = EmailNotValidException("Invalid email format")
        assert isinstance(exception, Exception)
        assert str(exception) == "Invalid email format"

    def test_supabase_rls_violation_exception(self):
        """Test SupabaseRLSViolationException instantiation."""
        exception = SupabaseRLSViolationException("RLS policy violation")
        assert isinstance(exception, Exception)
        assert str(exception) == "RLS policy violation"

    def test_supabase_duplicate_key_constraint_exception(self):
        """Test SupabaseDuplicateKeyConstraintException instantiation."""
        exception = SupabaseDuplicateKeyConstraintException("Duplicate key violation")
        assert isinstance(exception, Exception)
        assert str(exception) == "Duplicate key violation"

    def test_supabase_null_value_insertion_exception(self):
        """Test SupabaseNullValueInsertionException instantiation."""
        exception = SupabaseNullValueInsertionException("Null value insertion error")
        assert isinstance(exception, Exception)
        assert str(exception) == "Null value insertion error"

    def test_invalid_credentials_exception(self):
        """Test InvalidCredentialsException instantiation."""
        exception = InvalidCredentialsException("Invalid credentials provided")
        assert isinstance(exception, Exception)
        assert str(exception) == "Invalid credentials provided"

    def test_user_not_logged_exception(self):
        """Test UserNotLoggedException instantiation."""
        exception = UserNotLoggedException("User not logged in")
        assert isinstance(exception, Exception)
        assert str(exception) == "User not logged in"

    def test_all_exceptions_without_message(self):
        """Test all simple exceptions can be instantiated without message."""
        exceptions = [
            GenericException,
            WrongCredentialsException,
            WrongPasswordException,
            UserAlreadyExistsException,
            EmailNotConfirmedException,
            UserNotAllowedException,
            SupabaseApiException,
            PasswordNotEqualException,
            InputNotFilledException,
            InvalidInputException,
            EmailNotValidException,
            SupabaseRLSViolationException,
            SupabaseDuplicateKeyConstraintException,
            SupabaseNullValueInsertionException,
            InvalidCredentialsException,
            UserNotLoggedException
        ]

        for exception_class in exceptions:
            exception = exception_class()
            assert isinstance(exception, Exception)

    def test_exceptions_can_be_raised_and_caught(self):
        """Test that all exceptions can be raised and caught properly."""
        exceptions_and_messages = [
            (GenericException, "Generic error"),
            (WrongCredentialsException, "Wrong credentials"),
            (WrongPasswordException, "Wrong password"),
            (UserAlreadyExistsException, "User exists"),
            (EmailNotConfirmedException, "Email not confirmed"),
            (UserNotAllowedException, "User not allowed"),
            (SupabaseApiException, "Supabase error"),
            (PasswordNotEqualException, "Passwords not equal"),
            (InputNotFilledException, "Input not filled"),
            (InvalidInputException, "Invalid input"),
            (EmailNotValidException, "Email not valid"),
            (SupabaseRLSViolationException, "RLS violation"),
            (SupabaseDuplicateKeyConstraintException, "Duplicate key"),
            (SupabaseNullValueInsertionException, "Null value insertion"),
            (InvalidCredentialsException, "Invalid credentials"),
            (UserNotLoggedException, "User not logged")
        ]

        for exception_class, message in exceptions_and_messages:
            with pytest.raises(exception_class) as exc_info:
                raise exception_class(message)
            assert str(exc_info.value) == message


class TestExceptionEdgeCases:
    """Test suite for edge cases and error scenarios."""

    def test_app_error_with_non_string_values(self):
        """Test AppError with non-string values."""
        error_dict = {
            "message": 123,
            "code": 456,
            "hint": True,
            "details": ["list", "of", "values"]
        }

        app_error = AppError(error_dict)

        assert app_error.message == 123
        assert app_error.code == 456
        assert app_error.hint is True
        assert app_error.details == ["list", "of", "values"]

    def test_app_error_with_extra_fields(self):
        """Test AppError ignores extra fields in constructor but preserves them in json."""
        error_dict = {
            "message": "Test message",
            "code": "TEST_001",
            "extra_field_1": "extra_value_1",
            "extra_field_2": "extra_value_2"
        }

        app_error = AppError(error_dict)

        # Extra fields should not be accessible as attributes
        assert not hasattr(app_error, "extra_field_1")
        assert not hasattr(app_error, "extra_field_2")

        # But should be preserved in json
        assert app_error.json() == error_dict

    def test_app_error_repr_with_very_long_strings(self):
        """Test AppError representation with very long strings."""
        long_message = "Very long error message " * 100
        long_code = "VERY_LONG_CODE_" * 10

        error_dict = {
            "message": long_message,
            "code": long_code
        }

        app_error = AppError(error_dict)
        repr_string = repr(app_error)

        assert long_message in repr_string
        assert long_code in repr_string

    def test_exceptions_with_unicode_characters(self):
        """Test exceptions with unicode characters."""
        unicode_message = "Error with émojis 🚀 and special chars: ñáéíóú"

        exception = GenericException(unicode_message)
        assert str(exception) == unicode_message

        app_error = AppError({"message": unicode_message})
        assert app_error.message == unicode_message

    def test_app_error_with_empty_strings(self):
        """Test AppError with empty strings."""
        error_dict = {
            "message": "",
            "code": "",
            "hint": "",
            "details": ""
        }

        app_error = AppError(error_dict)

        assert app_error.message == ""
        assert app_error.code == ""
        assert app_error.hint == ""
        assert app_error.details == ""

        # Should show "Empty error" since all strings are empty
        assert repr(app_error) == "Empty error"