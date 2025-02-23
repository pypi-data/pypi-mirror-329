from typing import Any, Iterable, List


class WombatException(Exception):
    """Base class for errors thrown by our package"""


class InvalidParameterTypeException(WombatException):
    """Exception thrown when an parameter is of the wrong type"""

    def __init__(
        self,
        parameter_name: str,
        parameter_value: Any,
        function_name: str,
        actual_type: type,
        allowed_types: set[type],
    ):
        super().__init__(parameter_name, function_name, actual_type, allowed_types)
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.function_name = function_name
        self.actual_type = actual_type
        self.allowed_types = allowed_types

    def __str__(self) -> str:
        return f"""
                Invalid Parameter Type Exception:
                    {self.parameter_name} to function {self.function_name} is of invalid type {self.actual_type}
                    Allowed Types: {self.allowed_types}"
            """


class InvalidParameterException(WombatException):
    """Exception thrown when an parameter is of the right type, but has an unacceptable value"""

    def __init__(
        self,
        parameter_name: str,
        parameter_value: Any,
        function_name: str,
        expected_values: Any,
    ):
        super().__init__(parameter_name, function_name)
        self.parameter_name = parameter_name
        self.function_name = function_name
        self.parameter_value = parameter_value
        self.expected_values = expected_values

    def __str__(self) -> str:
        return f"Parameter '{self.parameter_name}' to function {self.function_name} has value {self.parameter_value} which is not within the accepted values of {self.expected_values}"

class MissingParameterException(WombatException):
    """Exception thrown when an parameter is missing"""

    def __init__(
        self,
        function_name: str,
        parameter_names: Iterable[str],
    ):
        super().__init__(parameter_names, function_name)
        self.parameter_names = parameter_names
        self.function_name = function_name

    def __str__(self) -> str:
        result = ""
        for parameter_name in self.parameter_names:
            result += f"Parameter {parameter_name} is missing from function {self.function_name}\n"

        return result
