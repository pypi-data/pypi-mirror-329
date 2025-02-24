from typing import Any

import pytest

from cache_register import register


@pytest.fixture
def _clear_global_register() -> None:
    register._global_dict_register = dict()


@pytest.fixture
def primary_register() -> register.Register[Any]:
    return register.Register[Any]("primary")


@pytest.fixture
def secondary_register() -> register.Register[Any]:
    return register.Register[Any]("secondary")


class TestRegister:
    def test_register(
        self,
        _clear_global_register: None,
        primary_register: register.Register[Any],
        secondary_register: register.Register[Any],
    ) -> None:
        @primary_register.register("a")
        class A:
            pass

        assert primary_register.get("a") == A
        assert secondary_register.get("a") is None

    def test_register_many_objects_in_multiple_registers(
        self,
        _clear_global_register: None,
        primary_register: register.Register[Any],
        secondary_register: register.Register[Any],
    ) -> None:
        @primary_register.register("a")
        class A:
            pass

        @primary_register.register("b")
        class B:
            pass

        @secondary_register.register("c")
        class C:
            pass

        assert primary_register.get("a") == A
        assert primary_register.get("b") == B
        assert secondary_register.get("c") == C

        assert secondary_register.get("a") is None
        assert secondary_register.get("b") is None
        assert primary_register.get("c") is None

    def test_registering_multiple_objects_with_the_same_key(
        self, _clear_global_register: None, primary_register: register.Register[Any]
    ) -> None:
        @primary_register.register("a")
        class A:
            pass

        assert primary_register.get("a") == A
        with pytest.raises(register.DuplicateRegisterEntry) as e:

            @primary_register.register("a")
            class _:
                pass

        assert (
            e.value.args[0]
            == "An object with the key 'a' already exists in register 'primary'."
        )
