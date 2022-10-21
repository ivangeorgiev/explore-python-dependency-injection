def registered(registry):
    def decorator(cls):
        def cls_factory(*args, **kwargs):
            instance = cls(*args, **kwargs)
            registry.append(instance)
            return instance

        return cls_factory

    return decorator


import pytest


class FakeClass:
    pass


class TestRegisteredDecorator:
    @pytest.fixture(name="registry")
    def given_registry(self):
        return []

    @pytest.fixture(name="decorated")
    def given_decorated(self, registry):
        return registered(registry)(FakeClass)

    def test_given_decorated_class_when_create_instance_then_instance_is_in_registry(
        self, registry, decorated
    ):
        instance = decorated()
        assert isinstance(instance, FakeClass)
        assert instance in registry


"""
Example usage:

orders = []

@registered(orders)
class Order:
    ...

order1 = Order()
assert order1 in orders
"""
