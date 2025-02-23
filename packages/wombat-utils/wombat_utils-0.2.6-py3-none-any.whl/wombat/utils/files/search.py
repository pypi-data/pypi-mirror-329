from typing import List, Optional

import sys
from pathlib import Path

from wombat.utils.errors.decorators import enforce_type_hints_contracts
from wombat.utils.errors.exceptions import InvalidParameterException

TARGET_TYPES: List[str] = ["file", "dir"]


class Target:
    @enforce_type_hints_contracts
    def __init__(self, value: str, target_type: str):
        self.value = value
        if target_type not in TARGET_TYPES:
            raise InvalidParameterException(
                parameter_name="target_type",
                parameter_value=target_type,
                # * NOTE: Intentional private call to get coroutine name,
                # * can be replaced if a more optimal solution is found
                function_name=sys._getframe().f_code.co_name,
                expected_values=",".join(TARGET_TYPES),
            )
        self.target_type = target_type


@enforce_type_hints_contracts
def upward_search(target: Target, bottom: Path, top: Path) -> Optional[Path]:
    """
    Search a directory tree, from bottom to top, and return first path
    matching the target.
    """
    # Get files in current dir
    paths: List[Path] = list(bottom.iterdir())
    dirs: List[Path] = []
    files: List[Path] = []

    for path in paths:
        if not path.is_file() and target.target_type == "dir":
            if path.stem == target.value:
                return path
            dirs.append(path)
        elif target.target_type == "file":
            if path.name == target.value:
                return path
            files.append(path)

    if bottom == top:
        return None

    # Literally no idea why mypy thinks I'm returning Any here
    # Have attempted many things to "fix" that warning
    return upward_search(target=target, bottom=Path(bottom.parent), top=top)  # type: ignore[no-any-return]
