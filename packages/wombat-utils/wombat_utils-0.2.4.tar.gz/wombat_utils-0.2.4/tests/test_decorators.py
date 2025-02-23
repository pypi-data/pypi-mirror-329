import pytest
from hypothesis import given, strategies as st, settings
from wombat.utils.errors.decorators import (
    enforce_type_hints_contracts,
)
from type_lens.callable_view import CallableView
from type_lens.type_view import TypeView
from typing import (
    Any,
    Dict,
    List,
    Callable,
    Union,
    TypeVar,
    Optional,
    Generic,
    Annotated,
)
from datetime import timedelta
from pydantic import BaseModel
from annotated_types import Ge


# Apply the decorator to the functions we want to enforce type contracts on
@enforce_type_hints_contracts
def process_data(data: list[int], multiplier: float):
    print(f"process_data called with data: {data}, multiplier: {multiplier}")


@enforce_type_hints_contracts
def process_mapping(mapping: dict[str, int], flag: bool):
    print(f"process_mapping called with mapping: {mapping}, flag: {flag}")


@enforce_type_hints_contracts
def process_optional_data(data: list[int] | None, multiplier: float | None):
    print(f"process_optional_data called with data: {data}, multiplier: {multiplier}")


@enforce_type_hints_contracts
def process_complex_data(data: Dict[str, Dict[str, List[int]]]):
    print(f"process_complex_data called with data: {data}")


T = TypeVar("T", bound=BaseModel)


class ModelQueue(BaseModel, Generic[T]):
    name: str
    joinable: bool = False


@enforce_type_hints_contracts
def process_typevars(data: Optional[ModelQueue[T]]) -> List[T]:
    print(f"process_typevars called with data: {data}")
    return data


@enforce_type_hints_contracts
def process_annotated_types(data: List[Annotated[int, Ge(0)]]):
    print(f"process_annotated_types called with data: {data}")


# Improved helper to generate Hypothesis strategies based on TypeView
def generate_strategy_from_typeview(type_view: TypeView) -> Any:
    """
    Generate a Hypothesis strategy based on the TypeView object.
    """
    if type_view.is_literal:
        # Handle Literal types
        return st.sampled_from([arg for arg in type_view.args])
    elif type_view.is_none_type:
        # Handle None type
        return st.none()
    elif type_view.is_union:
        # Handle Union types by generating strategies for each inner type
        return st.one_of(
            [
                generate_strategy_from_typeview(inner_type)
                for inner_type in type_view.inner_types
            ]
        )
    elif type_view.is_optional:
        # Optional types are Unions that include None
        return st.one_of(
            st.none(), generate_strategy_from_typeview(type_view.strip_optional())
        )
    elif type_view.origin is list or type_view.raw is list:
        if type_view.inner_types:
            # Handle list types with inner types
            return st.lists(
                generate_strategy_from_typeview(type_view.inner_types[0]),
                min_size=1,
                max_size=100,
            )
        else:
            # Default for collections with unknown inner types
            return st.lists(
                generate_strategy_from_typeview(TypeView(Any))
            )  # Default to list of strings for general collections
    elif type_view.origin is dict or type_view.raw is dict:
        # Handle mapping types (e.g., Dict)
        if not type_view.inner_types:
            return st.dictionaries(
                st.text(min_size=1),
                st.text(min_size=1),
                min_size=1,
                max_size=10,
            )
        key_type, value_type = type_view.inner_types
        return st.dictionaries(
            generate_strategy_from_typeview(key_type),
            generate_strategy_from_typeview(value_type),
            min_size=1,
            max_size=10,
        )
    elif type_view.is_subtype_of(float):
        # Handle float type
        return st.floats(allow_nan=False, allow_infinity=False)
    elif type_view.is_subtype_of(bool):
        # Handle boolean type
        return st.booleans()
    elif type_view.is_subtype_of(int):
        # Handle integer type
        return st.integers()
    elif type_view.is_subtype_of(str):
        # Handle string type
        return st.text(min_size=1)
    elif type_view.repr_type == "Any":
        # Handle Any type
        return (
            st.integers()
            | st.floats()
            | st.ip_addresses()
            | st.text()
            | st.none()
            | st.booleans()
            | st.emails()
            | st.dates()
            | st.times()
            | st.datetimes()
            | st.uuids()
            | st.binary()
            | st.decimals()
            | st.fractions()
        )
    elif type_view.is_type_var:
        return generate_strategy_from_typeview(TypeView(type_view.raw.__bound__))
    elif isinstance(type_view.raw, type) and issubclass(type_view.raw, BaseModel):
        raise NotImplementedError(
            f"Unsupported type: {type_view}, TODO: Implement model strategy using polyfactory"
        )
    else:
        raise NotImplementedError(f"Unsupported type: {type_view}")


def generate_strategies_from_function(func: Callable) -> Dict[str, Any]:
    """
    Generate a dictionary of Hypothesis strategies for each parameter of a function
    using the CallableView and TypeView.
    """
    callable_view = CallableView.from_callable(func)
    strategies = {}

    for param in callable_view.parameters:
        strategies[param.name] = generate_strategy_from_typeview(param.type_view)

    return strategies


@given(**generate_strategies_from_function(process_data))
def test_process_data_hypothesis(data, multiplier):
    process_data(data, multiplier)


@given(**generate_strategies_from_function(process_mapping))
def test_process_mapping_hypothesis(mapping, flag):
    process_mapping(mapping, flag)


@given(**generate_strategies_from_function(process_optional_data))
def test_process_optional_data_hypothesis(data, multiplier):
    process_optional_data(data, multiplier)


@given(**generate_strategies_from_function(process_complex_data))
def test_process_complex_data_hypothesis(data):
    process_complex_data(data)


@pytest.mark.parametrize(
    "data, multiplier, expected_exception",
    [
        pytest.param([1, 2, "banana"], 2.5, TypeError, id="invalid_string_in_list"),
        pytest.param([1, 2, 3], "string", TypeError, id="invalid_multiplier_string"),
    ],
)
def test_process_data_invalid_cases(data, multiplier, expected_exception):
    with pytest.raises(expected_exception):
        process_data(data, multiplier)


# Invalid test cases for process_mapping
@pytest.mark.parametrize(
    "mapping, flag, expected_exception",
    [
        pytest.param(
            {"a": 1, "b": "banana"}, True, TypeError, id="invalid_string_in_dict"
        ),
        pytest.param({"a": 1, "b": 2}, "not_bool", TypeError, id="invalid_flag_string"),
    ],
)
def test_process_mapping_invalid_cases(mapping, flag, expected_exception):
    with pytest.raises(expected_exception):
        process_mapping(mapping, flag)


@enforce_type_hints_contracts
def super_hard(
    a: Dict[
        Union[str, int], Union[Dict[str, List[Dict[str, Union[int, float]]]], List[int]]
    ],
):
    print(f"super_hard called with a: {a}")


@settings(deadline=timedelta(seconds=5))
@given(**generate_strategies_from_function(super_hard))
def test_super_hard(a):
    super_hard(a)


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(ModelQueue[int](name="billy", joinable=False), id="valid_list"),
    ],
)
def test_process_typevars(data):
    process_typevars(data)


@pytest.mark.skip(
    reason="TODO: implement a strategy for Annotated types, currently feeds negative integers despite positive values being required"
)
@given(**generate_strategies_from_function(process_annotated_types))
def test_process_annotated_types(data):
    process_annotated_types(data)


@pytest.mark.parametrize(
    "data, expected_exception",
    [
        pytest.param([1, 2, 1, 3], None, id="valid"),
        pytest.param([1, 2, -1, 3], TypeError, id="invalid"),
    ],
)
def test_process_annotated_type_manual(data, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            process_annotated_types(data)
    else:
        process_annotated_types(data)


@pytest.mark.parametrize(
    "value, result",
    [
        pytest.param(TypeView(int), "integers()", id="int"),
        pytest.param(TypeView(str), "text(min_size=1)", id="str"),
        pytest.param(TypeView(bool), "booleans()", id="bool"),
        pytest.param(
            TypeView(float), "floats(allow_nan=False, allow_infinity=False)", id="float"
        ),
        pytest.param(TypeView(None), "none()", id="None"),
        pytest.param(
            TypeView(list),
            "lists(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(one_of(integers(), floats()), ip_addresses()), text()), none()), booleans()), emails()), dates()), times()), datetimes()), uuids()), binary()), decimals()), fractions()))",
            id="list",
        ),
        pytest.param(
            TypeView(dict),
            "dictionaries(keys=text(min_size=1), values=text(min_size=1), min_size=1, max_size=10)",
            id="dict",
        ),
        pytest.param(
            TypeView(Union[int, str]),
            "one_of(integers(), text(min_size=1))",
            id="Union",
        ),
        pytest.param(
            TypeView(Optional[int]),
            "one_of(integers(), none())",
            id="Optional",
        ),
        # pytest.param(TypeView(Annotated[int, Ge(0)]), id="Annotated"),
    ],
)
def test_generate_strategy_from_type_view(value: TypeView, result):
    # integers, text, booleans, floats, None, lists, dictionaries, unions
    assert str(generate_strategy_from_typeview(value)) == result
