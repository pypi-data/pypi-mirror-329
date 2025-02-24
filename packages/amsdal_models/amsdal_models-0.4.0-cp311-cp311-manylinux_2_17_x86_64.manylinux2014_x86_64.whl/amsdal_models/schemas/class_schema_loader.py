from collections.abc import Callable
from typing import TYPE_CHECKING

from amsdal_utils.schemas.interfaces import BaseSchemaLoader
from amsdal_utils.schemas.interfaces import ModulePathType
from amsdal_utils.schemas.schema import ObjectSchema

from amsdal_models.classes.relationships.constants import FOREIGN_KEYS
from amsdal_models.classes.relationships.helpers.deferred_foreign_keys import complete_deferred_foreign_keys
from amsdal_models.classes.relationships.helpers.deferred_many_to_many import complete_deferred_many_to_many
from amsdal_models.classes.relationships.helpers.deferred_primary_keys import complete_deferred_primary_keys
from amsdal_models.classes.relationships.meta.references import build_fk_db_fields

if TYPE_CHECKING:
    from amsdal_models.classes.model import Model


class ClassSchemaLoader(BaseSchemaLoader):
    def __init__(
        self,
        module_path: ModulePathType,
        class_filter: Callable[[type['Model']], bool] | None = None,
    ) -> None:
        self._module_path = module_path
        self._class_filter = class_filter or (lambda cls: True)  # noqa: ARG005

    @property
    def schemas_per_module(self) -> dict[ModulePathType, list[ObjectSchema]]:
        return {self._module_path: self.load()}

    def load(self) -> list[ObjectSchema]:
        from amsdal_models.schemas.object_schema import model_to_object_schema

        return [model_to_object_schema(model_class) for model_class in self._load_classes()]

    def load_sorted(self) -> tuple[list[ObjectSchema], list[ObjectSchema]]:
        """
        Load object schemas sorted by dependencies.
        Returns: tuple of two elements, the first one is list of all sorted object schemas and the
                second one is list of schema that have cycle dependencies.
        """
        from amsdal_models.schemas.object_schema import model_to_object_schema

        _classes, _cycles = _sort_classes(self._load_classes())

        for model_class in _classes:
            _schema = model_to_object_schema(model_class)

            if model_class in _cycles:
                delattr(_schema, 'foreign_keys')

        return (
            [model_to_object_schema(model_class) for model_class in _classes],
            [model_to_object_schema(model_class) for model_class in _cycles],
        )

    def _load_classes(self) -> list[type['Model']]:
        from amsdal_models.classes.class_loader import ModelClassLoader

        model_class_loader = ModelClassLoader(self._module_path)
        return [_class for _class in model_class_loader.load(unload_module=True) if self._class_filter(_class)]


class ClassMultiDirectoryJsonLoader(BaseSchemaLoader):
    def __init__(
        self,
        module_paths: list[ModulePathType],
        class_filter: Callable[[type['Model']], bool] | None = None,
    ) -> None:
        self._module_paths = module_paths
        self._schemas_per_module: dict[ModulePathType, list[ObjectSchema]] = {}
        self._classes_per_module: dict[ModulePathType, list[type[Model]]] = {}
        self._class_filter = class_filter or (lambda cls: True)  # noqa: ARG005

    @property
    def schemas_per_module(self) -> dict[ModulePathType, list[ObjectSchema]]:
        return self._schemas_per_module

    def load(self) -> list[ObjectSchema]:
        from amsdal_models.schemas.object_schema import model_to_object_schema

        return [model_to_object_schema(model_class) for model_class in self._load_classes()]

    def load_sorted(self) -> tuple[list[ObjectSchema], list[ObjectSchema]]:
        from amsdal_models.schemas.object_schema import model_to_object_schema

        _classes, _cycles = _sort_classes(self._load_classes())

        for model_class in _classes:
            _schema = model_to_object_schema(model_class)

            if model_class in _cycles:
                delattr(_schema, 'foreign_keys')

        return (
            [model_to_object_schema(model_class) for model_class in _classes],
            [model_to_object_schema(model_class) for model_class in _cycles],
        )

    def _load_classes(self) -> list[type['Model']]:
        from amsdal_models.classes.class_loader import ModelClassLoader

        all_classes = []

        for _module_path in self._module_paths:
            model_class_loader = ModelClassLoader(_module_path)
            _classes = [_class for _class in model_class_loader.load(unload_module=True) if self._class_filter(_class)]
            all_classes.extend(_classes)
            self._classes_per_module[_module_path] = _classes
        return all_classes


def _sort_classes(
    classes: list[type['Model']],
) -> tuple[list[type['Model']], list[type['Model']]]:  # Changed return type for cycles
    """
    Sorts model classes based on their dependencies and detects circular dependencies.
    Returns (sorted_models, models_in_cycles).
    """
    # Build dependency graph
    graph: dict[str, set[str]] = {model.__name__: set() for model in classes}
    model_map = {model.__name__: model for model in classes}

    for model in classes:
        complete_deferred_primary_keys(model)
        complete_deferred_foreign_keys(model)
        complete_deferred_many_to_many(model)

        fks = getattr(model, FOREIGN_KEYS, None) or []

        for fk in fks:
            fk_annotation = model.model_fields[fk].annotation
            fk_type, _, _ = build_fk_db_fields(fk, fk_annotation)

            if not isinstance(fk_type, type):
                msg = f'Expected fk_type to be a type, got {type(fk_type)}'
                raise ValueError(msg)

            # Add to graph only if it's not a self-reference
            if fk_type.__name__ != model.__name__:
                graph[model.__name__].add(fk_type.__name__)

    # Find cycles
    cycles: set[str] = set()  # Changed to set of model names
    visited = set()
    path: list[str] = []

    def dfs(node: str) -> None:
        if node not in graph:
            # ignore external models
            return

        if node in path:
            cycle_start = path.index(node)
            cycle = path[cycle_start:]
            # Only add models if it involves more than one model
            if len(cycle) > 1:
                cycles.update(cycle)  # Add all models in cycle to the set
            return

        if node in visited:
            return

        visited.add(node)
        path.append(node)

        for neighbor in list(graph[node]):
            dfs(neighbor)

        path.pop()

    # Detect cycles
    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)

    # Topological sort
    sorted_models = []
    visited = set()

    def topo_sort(node: str) -> None:
        if node not in graph:
            return

        if node in visited:
            return

        visited.add(node)

        for dep in list(graph[node]):
            topo_sort(dep)

        sorted_models.append(model_map[node])

    for model in classes:
        if model.__name__ not in visited:
            topo_sort(model.__name__)

    # Convert cycle model names back to model classes
    cyclic_models = [model_map[name] for name in cycles]

    return sorted_models, cyclic_models
