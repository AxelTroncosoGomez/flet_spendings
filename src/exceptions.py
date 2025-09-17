from typing import Dict, Optional, Any

class AppError(Exception):
	"""
	Base exception for all App errors.
	"""

	__raw_error: Dict[str, str]
	message: Optional[str]
	"""The error message."""
	code: Optional[str]
	"""The error code."""
	hint: Optional[str]
	"""The error hint."""
	details: Optional[str]
	"""The error details."""

	def __init__(self, error: Dict[str, Any]) -> None:
		self.__raw_error = error
		self.message = error.get("message")
		self.code = error.get("code")
		self.hint = error.get("hint")
		self.details = error.get("details")
		Exception.__init__(self, str(self))

	def __repr__(self) -> str:
		error_text = f"Error {self.code}:" if self.code else ""
		message_text = f"\nMessage: {self.message}" if self.message else ""
		hint_text = f"\nHint: {self.hint}" if self.hint else ""
		details_text = f"\nDetails: {self.details}" if self.details else ""
		complete_error_text = f"{error_text}{message_text}{hint_text}{details_text}"
		return complete_error_text or "Empty error"

	def json(self) -> Dict[str, str]:
		"""Convert the error into a dictionary.

		Returns:
			:class:`dict`
		"""
		return self.__raw_error


class GenericException(Exception):
	pass


class WrongCredentialsException(Exception):
	pass


class WrongPasswordException(Exception):
	pass


class UserAlreadyExistsException(Exception):
	pass


class EmailNotConfirmedException(Exception):
	pass


class UserNotAllowedException(Exception):
	pass


class SupabaseApiException(Exception):
	pass


class PasswordNotEqualException(Exception):
	pass


class InputNotFilledException(Exception):
	pass

class InvalidInputException(Exception):
	pass


class EmailNotValidException(Exception):
	pass


class SupabaseRLSViolationException(Exception):
	pass


class SupabaseDuplicateKeyConstraintException(Exception):
	pass


class SupabaseNullValueInsertionException(Exception):
	pass

class InvalidCredentialsException(Exception):
	pass


class UserNotLoggedException(Exception):
	pass