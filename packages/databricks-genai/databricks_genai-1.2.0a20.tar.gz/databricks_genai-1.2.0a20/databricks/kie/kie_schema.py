"""Factory for KIE schemas"""
import hashlib
import json
from functools import reduce
from pathlib import Path
from types import UnionType
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union, cast, get_args, get_origin

from pydantic import BaseModel, ConfigDict, Field, create_model
from pydantic.fields import FieldInfo

_valid_types = Union[Type, Type[Any], UnionType]

PYTHON_TO_YAML_TYPE_MAP: Dict[_valid_types, str] = {
    str: "str",
    int: "int",
    bool: "bool",
    float: "float",
    Any: "any",
}

YAML_TO_PYTHON_TYPE_MAP: Dict[str, _valid_types] = {v: k for k, v in PYTHON_TO_YAML_TYPE_MAP.items()}

JSON_TO_PYTHON_TYPE_MAP: Dict[str, _valid_types] = {
    "string": str,
    "integer": int,
    "bool": bool,
    "number": float,
    "any": Any,
}

CONFIG_DICT = ConfigDict(protected_namespaces=())


def create_custom_model(model_name: str, **field_definitions: Tuple[type, FieldInfo]) -> type[BaseModel]:
    """Create a Pydantic model with custom configuration."""
    return create_model(model_name, __config__=CONFIG_DICT, **field_definitions)  # type: ignore


class ModelFactory:
    """Factory class for creating Pydantic models from JSON examples."""

    @staticmethod
    def infer_type(value: Optional[Any], key: str = "DyanmicModel") -> Union[type, Any]:
        """Infer Python/Pydantic type from a JSON value."""
        if value is None:
            return Any

        if isinstance(value, bool):
            return bool
        elif isinstance(value, int):
            return int
        elif isinstance(value, float):
            return float
        elif isinstance(value, str):
            return str
        elif isinstance(value, dict):
            return ModelFactory.create_model_from_dict(value, key)
        elif isinstance(value, list):
            if not value:  # Empty list
                return List[Any]
            # Infer type from first element
            element_type = ModelFactory.infer_type(value[0], key)
            return List[element_type]
        else:
            # in theory, all of the above supports all the necessary JSON types
            raise NotImplementedError(f"Type inference for {value} is not implemented")

    @staticmethod
    def create_field_definitions(data: Dict[str, Any]) -> Dict[str, Tuple[type, FieldInfo]]:
        """Create field definitions for Pydantic model."""
        fields = {}
        for key, value in data.items():
            field_type = ModelFactory.infer_type(value, key)

            # Create field definition
            # Without knowing otherwise, we'll call every  field "Optional"
            fields[key] = (Optional[field_type], Field(description=""))

        return fields

    @staticmethod
    def create_model_from_dict(data: Dict[str, Any], model_name: str = "DynamicModel") -> type[BaseModel]:
        """Create a Pydantic model from a dictionary."""
        if data == {}:
            raise ValueError("Cannot create a model from an empty dictionary")

        field_definitions = ModelFactory.create_field_definitions(data)

        # Ignore typing: field_definitions keeps matching with other kwargs that are reserved.
        # Unsure how to clean that up
        return create_custom_model(model_name, **field_definitions)

    @classmethod
    def from_examples(cls, examples: List[Dict[str, Any]], model_name: str = "DynamicModel") -> type[BaseModel]:
        """Build and validate JSON schema from a dictionary of examples."""
        all_keys = reduce(lambda x, y: x.union(y), [set(e.keys()) for e in examples])
        merged_dict = ModelFactory._merge_and_validate_examples(examples, all_keys)

        return cls.create_model_from_dict(merged_dict, model_name)

    @staticmethod
    def to_file(model: Type[BaseModel], path: Union[Path, str]) -> None:
        """Save a Pydantic model class schema to file."""

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Get full schema with definitions for nested models
        schema = model.model_json_schema()

        with path.open('w', encoding="utf-8") as f:
            json.dump({'_model_name': model.__name__, 'schema': schema}, f, indent=2)

    @classmethod
    def from_json_schema(cls, schema: Dict[str, Any], model_name: str = "DynamicModel") -> Type[BaseModel]:
        """
        Create a Pydantic model class from a JSON schema. Can optionally specify a model name.
        """

        def get_item_type(field_schema: Dict[str, Any]) -> _valid_types:
            """Get type from field schema, handling complex types like Optional[List[str]]."""

            # Handle anyOf (only allowed for Optional types)
            if 'anyOf' in field_schema:
                types = field_schema['anyOf']
                # Check if this is an Optional type (one null and one non-null)
                if len(types) == 2 and any(t.get('type') == 'null' for t in types):
                    # Get the non-null type - e.g. {'type': 'string'}
                    non_null_type = next(t for t in types if t.get('type') != 'null')
                    found_type = get_item_type(non_null_type)
                    return Optional[found_type]
                else:
                    # Raise an error for other Union types
                    raise TypeError("Union types are only allowed for Optional fields."
                                    f"Found schema: {field_schema}")

            # Handle direct type definitions
            if 'type' in field_schema:
                found_type = field_schema['type']

                # Handle arrays
                if found_type == 'array' and 'items' in field_schema:
                    if '$ref' in field_schema['items']:
                        ref_name = field_schema['items']['$ref'].split('/')[-1]
                        ref_schema = schema.get('$defs', {}).get(ref_name, {})
                        item_type = create_model_from_schema(ref_schema, ref_name)
                    else:
                        item_type = get_item_type(field_schema['items'])
                    return List[item_type]

                # Handle basic types
                return JSON_TO_PYTHON_TYPE_MAP.get(found_type, Any)

            return Any

        def create_model_from_schema(schema_data: Dict[str, Any], model_name: str) -> Type[BaseModel]:
            fields = {}

            for field_name, field_schema in schema_data.get('properties', {}).items():
                # Handle references to nested models
                if '$ref' in field_schema:
                    ref_name = field_schema['$ref'].split('/')[-1]
                    ref_schema = schema.get('$defs', {}).get(ref_name, {})
                    field_type = create_model_from_schema(ref_schema, ref_name)
                else:
                    field_type = get_item_type(field_schema)

                # Create field with description and title if present
                field_info = {}
                if 'description' in field_schema:
                    field_info['description'] = field_schema['description']
                if 'title' in field_schema:
                    field_info['title'] = field_schema['title']

                # Setup the type, Field tuple
                # Note all fields are considered "required", but some are nullable.
                fields[field_name] = (field_type, Field(**field_info))

            return create_custom_model(model_name, **fields)

        return create_model_from_schema(schema, model_name)

    @classmethod
    def from_file(cls, path: Union[Path, str]) -> Type[BaseModel]:
        """
        Load a Pydantic model class from a schema file.
        Expects the file to be in the format saved by `to_file`, that is,
        it should have a JSON schema and a model name.
        """

        path = Path(path)
        with path.open('r', encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_json_schema(data['schema'], data['_model_name'])

    @staticmethod
    def _merge_and_validate_examples(examples: List[Dict[str, Any]], all_keys: set[str]) -> Dict[str, Any]:
        """Merge and validate examples.
        
        The output of this is expected to be a valid dictionary such that all potential conflicts
        are solved and that Nones are removed.
        """

        def _handle_lists(list_examples: List[List[Any]]) -> List[Any]:
            flattened_list = list(filter(lambda z: z is not None, reduce(lambda x, y: x + y, list_examples)))

            if len(flattened_list) == 0:
                raise ValueError(f"Field {key} is missing examples or all values are None")

            inner_types = {type(e) for e in flattened_list}
            if len(inner_types) > 1:
                raise ValueError(f"Field {key} has conflicting types in its lists: {inner_types}")

            if isinstance(flattened_list[0], dict):
                list_dict_keys = set(flattened_list[0].keys())
                if any(set(e.keys()) != list_dict_keys for e in flattened_list):
                    raise ValueError(f"Field {key} has conflicting keys across its list of dictionaries")

                return [ModelFactory._merge_and_validate_examples(flattened_list, list_dict_keys)]
            elif inner_types == {list}:
                return [_handle_lists(flattened_list)]
            return [flattened_list[0]]

        merged_dict = {}
        for key in all_keys:
            key_examples = [e[key] for e in examples if key in e and e[key] is not None]

            if len(key_examples) == 0:
                raise ValueError(f"Miss non-empty examples for the field {key}")

            types = {type(e) for e in key_examples}
            if len(types) > 1:
                raise ValueError(f"Field {key} has conflicting types: {types}")
            field_type = types.pop()

            if field_type == dict:
                dict_keys = set(key_examples[0].keys())
                for key_example in key_examples:
                    if set(key_example.keys()) != dict_keys:
                        raise ValueError(f"Field {key} has conflicting keys across its dictionaries")

                merged_dict[key] = ModelFactory._merge_and_validate_examples(key_examples, set(key_examples[0].keys()))
            elif field_type == list:
                merged_dict[key] = _handle_lists(key_examples)
            else:
                merged_dict[key] = key_examples[0]
        return merged_dict


T = TypeVar('T', bound=BaseModel)


class ModelManager:
    """Manager for editing fields on a Pydantic model"""

    def __init__(self,
                 model: Type[T],
                 parent: Optional['ModelManager'] = None,
                 field_name: Optional[str] = None) -> None:
        self.model = model
        self.parent = parent
        self.field_name = field_name

        if (self.parent is None) is not (self.field_name is None):
            raise ValueError("Must specify both `parent` and `field_name` if one of them is specified")

    def __getitem__(self, field_name: str) -> 'ModelManager':
        if field_name not in self.model.model_fields:
            raise KeyError(f"Field {field_name} not found")

        field = self.model.model_fields[field_name]
        if not (isinstance(field.annotation, type) and issubclass(field.annotation, BaseModel)):
            raise TypeError(f"Field {field_name} is not a nested model")

        return ModelManager(field.annotation, self, field_name)

    @staticmethod
    def _copy_field(f: FieldInfo, **updates) -> Tuple[type, FieldInfo]:
        annotation = updates.pop("annotation", f.annotation)
        copied = {
            "description": f.description,
            "title": f.title,
            "default": f.default,
            "json_schema_extra": f.json_schema_extra,
        }
        copied.update(**updates)
        return (annotation, Field(**copied))

    def _update_model_with_fields(self, **fields: Tuple[type, FieldInfo]) -> Type[BaseModel]:
        new_model = create_custom_model(f"{self.model.__name__}", **fields)  # type: ignore
        self.model = cast(Type[T], new_model)
        return self.model

    def _update_parents(self) -> Type[BaseModel]:
        if not self.parent:
            return self.model

        current = self
        while current.parent is not None:
            assert current.field_name is not None
            current.parent.edit_types(**{current.field_name: current.model})
            current = current.parent
        return current.model

    def add_field(self, field_name: str, field_type: type, field_description: str = "") -> type[BaseModel]:

        # Add existing fields
        fields = {name: self._copy_field(field) for name, field in self.model.model_fields.items()}

        # Add new field
        fields[field_name] = (field_type, Field(description=field_description))

        self._update_model_with_fields(**fields)

        return self._update_parents()

    def edit_types(self, **type_updates: type) -> Type[BaseModel]:

        fields = {
            name: self._copy_field(field, annotation=type_updates.get(name, field.annotation))
            for name, field in self.model.model_fields.items()
        }
        self._update_model_with_fields(**fields)

        return self._update_parents()

    def edit_descriptions(self, **updates) -> Type[BaseModel]:

        fields = {
            name: self._copy_field(field, description=updates.get(name, field.description))
            for name, field in self.model.model_fields.items()
        }
        self._update_model_with_fields(**fields)

        return self._update_parents()


def model_to_dict(model: Type[BaseModel]) -> Dict[str, Any]:
    """Convert a Pydantic model to a dictionary describing its structure.

    Args:
        model: A Pydantic model class
        
    Returns:
        Dict with field names as keys and dicts containing:
            - type: String for basic types, dict for nested models, list for arrays 
            - description: Field description string
            
    Example:
        class User(BaseModel):
            name: str = Field(description="User name")
            tags: List[str]
            
        # Returns:
        {
            'name': {'type': 'str', 'description': 'User name'},
            'tags': {'type': [{'type': 'str'}], 'description': ''}
        }
    """
    output = {}
    for key, field in model.model_fields.items():
        type_ = field.annotation
        value: Dict[str, Any] = {"description": field.description or "", "required": True}
        if get_origin(type_) is Union:  # This is an optional field
            type_ = [t for t in get_args(type_) if t is not None][0]
            value["required"] = False

        if get_origin(type_) is list:
            args = get_args(type_)
            if isinstance(args[0], type) and issubclass(args[0], BaseModel):
                # This is an array of models
                type_value = [model_to_dict(args[0])]
            else:
                type_value = [{"type": PYTHON_TO_YAML_TYPE_MAP.get(args[0], "any")}]
        elif isinstance(type_, type) and issubclass(type_, BaseModel):
            # This is a nested model
            type_value = model_to_dict(type_)
        else:
            type_value = PYTHON_TO_YAML_TYPE_MAP.get(type_, "any")
        value['type'] = type_value
        output[key] = value
    return output


def dict_to_model(model_dict: Dict[str, Any]) -> Type[BaseModel]:
    """Create a Pydantic model from a dictionary describing its structure.

    Args:
        model_dict: Dict with field names as keys and field info dicts containing:
            - type: String for basic types, dict for nested models, list for arrays
            - description: Optional field description string
            
    Returns:
        A generated Pydantic model class with the specified structure
        
    Example:
        schema = {
            'name': {'type': 'str', 'description': 'User name'},
            'tags': {'type': [{'type': 'str'}]}
        }
        UserModel = dict_to_model(schema)
    """
    fields = {}
    for key, value in model_dict.items():
        description = value.get('description', '')
        required = value.get('required', True)

        requested_type = value.get('type')
        if not requested_type:
            raise ValueError(f"Field {key} is missing a type, please specify one in your schema.")

        type_ = Any
        if isinstance(requested_type, list):
            item = requested_type[0]
            if 'type' in item:
                requested_inner_type = item['type']
                if requested_inner_type not in YAML_TO_PYTHON_TYPE_MAP:
                    raise ValueError(f"Array field {key} has an unknown type: {requested_inner_type}. " +
                                     "Please update your schema to provide a valid type.")
                inner_type = YAML_TO_PYTHON_TYPE_MAP.get(requested_inner_type, Any)
                if inner_type == Any:
                    raise ValueError(f"Array field {key} has a type of any, which is not supported. " +
                                     "Please update your schema to provide a specific type.")

                type_ = List[inner_type]
            else:
                item_type = dict_to_model(item)
                type_ = List[item_type]
        elif isinstance(requested_type, dict):
            # Nested model
            type_ = dict_to_model(requested_type)
        elif requested_type in YAML_TO_PYTHON_TYPE_MAP:
            # Basic type
            type_ = YAML_TO_PYTHON_TYPE_MAP.get(requested_type)
        else:
            raise ValueError(
                f"Field {key} has an unknown type: {requested_type}. Please update your schema to provide a valid type."
            )

        if type_ == Any:
            raise ValueError(f"Field {key} has a type of any, which is not supported. " +
                             "Please update your schema to provide a specific type.")

        if not required:
            type_ = Optional[type_]
        fields[key] = (type_, Field(description=description))

    return create_custom_model("Model", **fields)


def get_schema_hash(response_format: Type[BaseModel]) -> str:
    schema = json.dumps(response_format.model_json_schema())
    return hashlib.md5(schema.encode()).hexdigest()[:8]
