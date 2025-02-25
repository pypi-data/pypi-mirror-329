from typing import Optional, List, Type, NamedTuple, Union, Tuple


class RegistryId(NamedTuple):
    name: str
    backend: str

    def __str__(self):
        return f"{self.name}-{self.backend}"

    @classmethod
    def factory(self, value: Union["RegistryId", str, Tuple]):
        if isinstance(value, RegistryId):
            return value
        if isinstance(value, str):
            return RegistryId(*value.split("-"))
        return RegistryId(*value)


class Registered:
    _SUBCLASS_REGISTRY = None

    RegistryId = RegistryId

    def __init_subclass__(
        cls,
        register: bool = True,
        registry_id: Union["RegistryId", str, Tuple, None] = None,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)

        # Ensures that not all subclasses share the same registry
        if cls._SUBCLASS_REGISTRY is None:
            cls._SUBCLASS_REGISTRY = dict()

        if not register:
            cls.__registry_id = None
            return

        # Register the subclass
        if registry_id is None:
            raise RuntimeError(f"Class {repr(cls)} is missing a `registry_id`")
        registry_id = RegistryId.factory(registry_id)
        ecls = cls._SUBCLASS_REGISTRY.get(registry_id)
        if ecls is not None:
            raise RuntimeError(
                f"Registry name {registry_id} is already taken by {repr(ecls)}"
            )
        cls.__registry_id = registry_id
        cls._SUBCLASS_REGISTRY[registry_id] = cls

    @classmethod
    def get_subclass_id(cls) -> Optional[RegistryId]:
        return cls.__registry_id

    @classmethod
    def get_subclass_ids(cls) -> List[RegistryId]:
        return list(cls._SUBCLASS_REGISTRY.keys())

    @classmethod
    def get_subclass_items(cls) -> List[RegistryId]:
        return list(cls._SUBCLASS_REGISTRY.items())

    @classmethod
    def get_subclasses(cls) -> List[Type["Registered"]]:
        return list(cls._SUBCLASS_REGISTRY.values())

    @classmethod
    def get_subclass(cls, registry_id: RegistryId) -> Type["Registered"]:
        registry_id = RegistryId.factory(registry_id)
        try:
            return cls._SUBCLASS_REGISTRY[registry_id]
        except KeyError:
            s = ", ".join(list(map(str, cls._SUBCLASS_REGISTRY)))
            raise RuntimeError(
                f"No class with registry name {registry_id} found. Available classes are {s}"
            )
