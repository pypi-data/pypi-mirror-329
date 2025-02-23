from typing import Any, Dict, Optional, Union, Callable, List
from copy import deepcopy
from wombat.utils.errors.decorators import enforce_type_hints_contracts


def concat_strategy(av: List[Any], bv: List[Any]) -> List[Any]:
    """
    Concatenate two values if they are both lists.
    """
    return av + bv if isinstance(av, list) and isinstance(bv, list) else [av, bv]


def override_strategy(av: Any, bv: Any) -> Any:
    """
    Override the first value with the second.
    """
    return deepcopy(bv)


def apply_strategy(av: Any, bv: Any, strategy: Optional[Union[str, Callable[[Any, Any], Any]]]) -> Any:
    """
    Apply the appropriate strategy to merge or override values.
    """
    if strategy == "concat":
        strategy = concat_strategy
    elif strategy == "override":
        strategy = override_strategy

    if callable(strategy):
        return strategy(av, bv)

    # Default behavior inferred from the types of av and bv
    if isinstance(av, dict) and isinstance(bv, dict):
        return deep_merge(av, bv)
    elif isinstance(av, list) and isinstance(bv, list):
        return concat_strategy(av, bv)
    else:
        return deepcopy(bv)

def deep_merge(
    a: Dict[str, Any],
    b: Dict[str, Any],
    strategies: Optional[Dict[str, Union[str, Callable[[Any, Any], Any]]]] = None,
) -> Dict[str, Any]:
    if strategies is None:
        strategies = {}
    result = deepcopy(a)
    for bk, bv in b.items():
        av = result.get(bk, None)
        current_strategy = strategies.get(bk, None)

        # Apply the appropriate strategy using `apply_strategy`
        result[bk] = apply_strategy(av, bv, current_strategy)

    return result
