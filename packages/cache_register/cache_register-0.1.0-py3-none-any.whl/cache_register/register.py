import warnings
from collections.abc import Callable
from typing import Any

_global_dict_register: dict[str, dict[str, Any]] = {}


class DuplicateRegisterEntry(Exception):
    pass


class InvalidObjectInRegister(Exception):
    pass


class UnspecifiedRegisterObjectType(Exception):
    pass


class Register[T]:
    def __init__(self, name: str) -> None:
        self._name = name
        if self._name not in _global_dict_register:
            _global_dict_register[self._name] = {}

    def register(self, key: str) -> Callable[[T], T]:
        def _(obj: T) -> Any:
            input_cls_parents = obj.__mro__  # type: ignore [attr-defined]
            try:
                required_cls_type = self.__orig_class__.__args__[0]   # type: ignore [attr-defined]
            except AttributeError:
                required_cls_type = object
                warnings.warn(
                    f"Register '{self._name}' has been defined without a specified type. "
                    f"This may cause unexpected behaviour.",
                )

            if required_cls_type not in input_cls_parents:
                raise InvalidObjectInRegister(
                    f"Attempted to register an objects of type '{input_cls_parents[1]}' "
                    f"in register '{self._name}'. This register can only contain "
                    f"objects of type '{required_cls_type.__name__}'."
                )

            if key in _global_dict_register[self._name]:
                raise DuplicateRegisterEntry(
                    f"An object with the key '{key}' "
                    f"already exists in register '{self._name}'."
                )

            _global_dict_register[self._name][key] = obj

            return obj

        return _

    def get(self, key: str) -> type | None:
        assert self._name in _global_dict_register, f"'{self._name}' is not in the list of known registers."
        sub_register = _global_dict_register[self._name]
        return sub_register.get(key)
