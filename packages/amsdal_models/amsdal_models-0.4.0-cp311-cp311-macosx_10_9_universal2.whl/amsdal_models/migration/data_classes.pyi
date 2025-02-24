from amsdal_models.classes.model import Model as Model
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.enums import ModuleType as ModuleType
from amsdal_utils.schemas.schema import ObjectSchema as ObjectSchema, PropertyData as PropertyData
from enum import Enum
from pathlib import Path

class Action(str, Enum):
    """
    Enumeration for different types of actions.

    Attributes:
        CREATED (str): Represents a created action.
        UPDATED (str): Represents an updated action.
        NO_ACTION (str): Represents no action.
    """
    CREATE: str
    UPDATE: str
    NO_ACTION: str

class ClassSaveResult:
    """
    Data class representing the result of a class save operation.

    Attributes:
        action (Action): The action performed during the save operation.
        instance (Model): The instance of the model that was saved.
    """
    action: Action
    instance: Model
    def __init__(self, action, instance) -> None: ...
    def __mypy-replace(*, action, instance) -> None: ...

class ClassUpdateResult:
    """
    Data class representing the result of a class update operation.

    Attributes:
        is_updated (bool): Indicates whether the class was updated.
        class_instance (Model): The instance of the model that was updated.
    """
    is_updated: bool
    class_instance: Model
    def __init__(self, is_updated, class_instance) -> None: ...
    def __mypy-replace(*, is_updated, class_instance) -> None: ...

class MigrateResult:
    """
    Data class representing the result of a migration operation.

    Attributes:
        class_instance (Model): The instance of the model that was migrated.
        is_table_created (bool): Indicates whether the table was created during the migration.
        is_data_migrated (bool): Indicates whether the data was migrated.
    """
    class_instance: Model
    is_table_created: bool
    is_data_migrated: bool
    def __init__(self, class_instance, is_table_created, is_data_migrated) -> None: ...
    def __mypy-replace(*, class_instance, is_table_created, is_data_migrated) -> None: ...

class MigrationFile:
    """
    Data class representing a migration file.

    Attributes:
        path (Path): The file path of the migration.
        type (ModuleType): The type of module the migration belongs to.
        number (int): The migration number.
        module (str | None): The module name, if applicable.
        applied_at (float | None): The timestamp when the migration was applied.
        stored_address (Address | None): The stored address associated with the migration.
    """
    path: Path
    type: ModuleType
    number: int
    module: str | None
    applied_at: float | None
    stored_address: Address | None
    @property
    def is_initial(self) -> bool:
        """
        Indicates whether this migration is the initial migration.

        Returns:
            bool: True if this is the initial migration, False otherwise.
        """
    def __init__(self, path, type, number, module, applied_at, stored_address) -> None: ...
    def __mypy-replace(*, path, type, number, module, applied_at, stored_address) -> None: ...

class ClassSchema:
    """
    Data class representing a class schema.

    Attributes:
        object_schema (ObjectSchema): The object schema associated with the class.
        type (ModuleType): The type of module the class belongs to.
    """
    object_schema: ObjectSchema
    type: ModuleType
    def __init__(self, object_schema, type) -> None: ...
    def __mypy-replace(*, object_schema, type) -> None: ...

class OperationTypes(str, Enum):
    """
    Enumeration for different types of operations.

    Attributes:
        CREATE_CLASS (str): Represents the operation to create a class.
        UPDATE_CLASS (str): Represents the operation to update a class.
        DELETE_CLASS (str): Represents the operation to delete a class.
    """
    CREATE_CLASS: str
    UPDATE_CLASS: str
    DELETE_CLASS: str

class MigrateOperation:
    """
    Data class representing a migration operation.

    Attributes:
        type (OperationTypes): The type of operation being performed.
        class_name (str): The name of the class involved in the migration.
        module_type (ModuleType): The type of schema associated with the migration.
        old_schema (ObjectSchema | PropertyData | None): The old schema before the migration, if applicable.
        new_schema (ObjectSchema | PropertyData | None): The new schema after the migration, if applicable.
    """
    type: OperationTypes
    class_name: str
    module_type: ModuleType
    old_schema: ObjectSchema | PropertyData | None
    new_schema: ObjectSchema | PropertyData | None
    def __init__(self, type, class_name, module_type, old_schema, new_schema) -> None: ...
    def __mypy-replace(*, type, class_name, module_type, old_schema, new_schema) -> None: ...

class MigrationDirection(str, Enum):
    """
    Enumeration for the direction of a migration.

    Attributes:
        FORWARD (str): Represents a forward migration.
        BACKWARD (str): Represents a backward migration.
    """
    FORWARD: str
    BACKWARD: str

class MigrationResult:
    """
    Data class representing the result of a migration.

    Attributes:
        direction (MigrationDirection): The direction of the migration.
        migration (MigrationFile): The migration file associated with the migration.
    """
    direction: MigrationDirection
    migration: MigrationFile
    def __init__(self, direction, migration) -> None: ...
    def __mypy-replace(*, direction, migration) -> None: ...
