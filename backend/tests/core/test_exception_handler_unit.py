from ecommerce.core.exception_handler import (
    _flatten_field_error,
    _split_message_and_details,
)


class TestSplitMessageAndDetails:
    def test_simple_detail_returns_message_and_no_details(self):
        msg, details = _split_message_and_details({"detail": "Not found."})
        assert msg == "Not found."
        assert details is None

    def test_field_error_preserves_full_data_in_details(self):
        payload = {"email": ["Invalid email."]}
        msg, details = _split_message_and_details(payload)
        assert msg == "email: Invalid email."
        assert details == payload

    def test_non_field_errors_strips_key_in_message(self):
        payload = {"non_field_errors": ["Passwords don't match."]}
        msg, details = _split_message_and_details(payload)
        assert msg == "Passwords don't match."
        assert details == payload

    def test_bare_list_is_wrapped_under_errors_key(self):
        msg, details = _split_message_and_details(["First.", "Second."])
        assert msg == "First."
        assert details == {"errors": ["First.", "Second."]}

    def test_nested_field_error_flattens_to_dotted_path(self):
        payload = {"address": {"city": ["City is required."]}}
        msg, details = _split_message_and_details(payload)
        assert msg == "address.city: City is required."
        assert details == payload


class TestFlattenFieldError:
    def test_simple_list_value(self):
        assert _flatten_field_error("email", ["Invalid."]) == "email: Invalid."

    def test_nested_dict_value(self):
        result = _flatten_field_error("address", {"city": ["Required."]})
        assert result == "address.city: Required."

    def test_list_of_dicts(self):
        result = _flatten_field_error("items", [{"qty": ["Must be 1+"]}])
        assert result == "items[0].qty: Must be 1+"