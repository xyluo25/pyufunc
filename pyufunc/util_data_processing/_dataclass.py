'''
##############################################################
# Created Date: Thursday, August 22nd 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

from dataclasses import dataclass, field, fields, make_dataclass, MISSING, is_dataclass, asdict
from typing import Any, List, Tuple, Type, Union, Dict
import copy


def dataclass_from_dict(name: str, data: Dict[str, Any]) -> Type:
    """Creates a dataclass with attributes and values based on the given dictionary.
    The dataclass will also support dictionary-like access via __getitem__ and __setitem__.

    Args:
        name (str): The name of the dataclass to create.
        data (Dict[str, Any]): A dictionary where keys are attribute names and values are attribute values.

    Example:
        >>> from pyufunc import dataclass_from_dict
        >>> data = {'name': 'Alice', 'age': 30, 'city': 'New York'}
        >>> Person = dataclass_from_dict('Person', data)
        >>> person = Person()
        >>> person.name
        'Alice'
        >>> person.age
        30
        >>> person.city
        'New York'

    Returns:
        Type: A dataclass with fields and values corresponding to the dictionary.
    """
    # Define a method for __getitem__ for dictionary-like access

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    # Define a method for __setitem__ for dictionary-like assignment
    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    # Define a method to convert the dataclass to a dictionary
    def as_dict(self):
        return asdict(self)

    # Extract fields and their types from the dictionary
    dataclass_fields = []
    for key, value in data.items():
        if isinstance(value, (list, dict, set)):  # For mutable types
            dataclass_fields.append(
                (key, type(value), field(default_factory=lambda v=value: v)))
        else:  # For immutable types
            dataclass_fields.append((key, type(value), field(default=value)))

    # Create the dataclass dynamically
    DataClass = make_dataclass(
        cls_name=name,
        fields=dataclass_fields,
        bases=(),
        namespace={'__getitem__': __getitem__,
                   '__setitem__': __setitem__,
                   'as_dict': as_dict}
    )

    # Instantiate the dataclass with the values from the dictionary
    return DataClass(**data)


def dataclass_creation(class_name: str, attributes: List[Union[Tuple[str, Type, Any], Tuple[str, Any]]]) -> Type:
    """Dynamically creates a dataclass with the given attributes.

    Args:
        class_name (str): The name of the dataclass to create.
        attributes (List[Union[Tuple[str, Type, Any], Tuple[str, Any]]]):
            A list of tuples where each tuple can be:
            - (attribute_name, type, default_value): The attribute name, type, and a default value.
            - (attribute_name, default_value): The attribute name and a default value, with the type inferred.

    Returns:
        Type: A new dataclass with the specified attributes.

    Example:
        >>> from pyufunc import dataclass_creation
        >>> attributes = [
        ...     ('attribute_one', int, 10),
        ...     ('attribute_two', "default_value"),  # Type inferred as str
        ...     ('attribute_three', float, 0.0)
        ... ]
        >>> DynamicClass = dataclass_creation('DynamicClass', attributes)
        >>> instance = DynamicClass(attribute_one=1)
        >>> print(instance.attribute_one)
        1
        >>> print(instance.attribute_two)
        default_value
        >>> print(instance.attribute_three)
        0.0
    """

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    # Define a method for __setitem__ for dictionary-like assignment
    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return asdict(self)

    processed_attributes = []

    for attr in attributes:
        if len(attr) == 2:
            # Name and default value provided, type is inferred
            processed_attributes.append((attr[0], type(attr[1]), attr[1]))
        elif len(attr) == 3:
            # Name, type, and default value provided
            processed_attributes.append((attr[0], attr[1], attr[2]))

    return make_dataclass(class_name, processed_attributes,
                          namespace={'__getitem__': __getitem__,
                                     '__setitem__': __setitem__,
                                     'as_dict': as_dict})


def dataclass_merge(dataclass_one: Type[Any], dataclass_two: Type[Any],
                    prefer: str = 'first',
                    *,
                    merged_class_name: str = "") -> Type[Any]:
    """Merges two dataclasses into a single new dataclass, handling duplicate attributes.

    Args:
        dataclass_one (Type[Any]): The first dataclass to merge.
        dataclass_two (Type[Any]): The second dataclass to merge.
        prefer (str): Specifies which dataclass to prefer in case of duplicate attributes.
            Defaults to 'first':
            - (option): 'first'
            - (option): 'second'

    Example:
        >>> from dataclasses import dataclass
        >>> from pyufunc import dataclass_merge
        >>> @dataclass
        ... class DataclassOne:
        ...     name: str
        ...     age: int = 30
        >>> @dataclass
        ... class DataclassTwo:
        ...     city: str
        ...     age: int = 40
        >>> MergedDataclass = dataclass_merge(DataclassOne, DataclassTwo, prefer='first')
        >>> MergedDataclass.age
        30
        >>> MergedDataclass = dataclass_merge(DataclassOne, DataclassTwo, prefer='second')
        >>> MergedDataclass.age
        40

    Returns:
        Type[Any]: A new dataclass that includes all fields from both dataclasses, with duplicates handled.

    """
    # Check if the inputs are dataclasses
    if not is_dataclass(dataclass_one) or not is_dataclass(dataclass_two):
        raise ValueError('Both inputs must be dataclasses')

    def get_fields(dataclass_inst: Type[Any]) -> List[Tuple[str, Type[Any], Any]]:
        result = []
        for f in fields(dataclass_inst):
            if f.default is not MISSING:
                result.append((f.name, f.type, f.default))
            elif f.default_factory is not MISSING:
                result.append((f.name, f.type, field(
                    default_factory=f.default_factory)))
            else:
                result.append((f.name, f.type))
        return result

    # Extract fields from both dataclasses
    fields_one = get_fields(dataclass_one)
    fields_two = get_fields(dataclass_two)

    # Combine the fields and handle duplicates
    all_fields = {}

    # Add fields from the first dataclass
    for name, typ, *default in fields_one:
        all_fields[name] = (typ, *default)

    # Add fields from the second dataclass, potentially overwriting
    for name, typ, *default in fields_two:
        if name in all_fields:
            if prefer == 'second':
                all_fields[name] = (typ, *default)
        else:
            all_fields[name] = (typ, *default)

    # Convert back to a list of tuples for make_dataclass
    final_fields = [(name, *info) for name, info in all_fields.items()]

    # Create the merged dataclass dynamically
    MergedDataclass = make_dataclass(
        cls_name=merged_class_name or None,
        fields=final_fields
    )

    return MergedDataclass


def dataclass_extend(base_dataclass: Type[Any],
                     additional_attributes: List[Tuple[str, Type[Any], Any]]) -> Type[Any]:
    """Creates a new dataclass by extending the base_dataclass with additional_attributes.

    Args:
        base_dataclass (dataclass): The base dataclass to extend.
        additional_attributes (list): A list of tuples in the form (name, type, default_value).
            or (name, default_value) to add to the base dataclass.

    Example:
        >>> from dataclasses import dataclass
        >>> from typing import List
        >>> from pyufunc import dataclass_extend
        >>> @dataclass
        ... class BaseDataclass:
        ...     name: str = 'base'

        >>> ExtendedDataclass = dataclass_extend(
        ...     base_dataclass=BaseDataclass,
        ...     additional_attributes=[('new_attr', List[int], [1, 2, 3])])
        >>> ExtendedDataclass

    Returns:
        dataclass: A new dataclass that includes fields from base_dataclass and additional_attributes.
    """

    # check inputs
    if not is_dataclass(base_dataclass):
        raise ValueError('base_dataclass must be a dataclass')

    for attr in additional_attributes:
        if len(attr) not in {2, 3}:
            raise ValueError('additional_attributes must be a list of tuples'
                             ' in the form (name, default_value) or (name, type, default_value)')

    # deepcopy the base dataclass
    base_dataclass_ = copy.deepcopy(base_dataclass)
    # base_dataclass_ = base_dataclass

    # Extract existing fields from the base dataclass
    base_fields = []
    for f in fields(base_dataclass_):
        if f.default is not MISSING:
            base_fields.append((f.name, f.type, f.default))
        elif f.default_factory is not MISSING:
            base_fields.append((f.name, f.type, field(
                default_factory=f.default_factory)))
        else:
            base_fields.append((f.name, f.type))

    # check if additional attributes:
    # if len == 2, adding Any as data type in the middle if the tuple
    # if len == 3, keep the original tuple
    additional_attributes = [
        val if len(val) == 3 else (val[0], Any, val[1])
        for val in additional_attributes
    ]

    # Combine base fields with additional attributes
    all_fields = base_fields + additional_attributes

    new_dataclass = make_dataclass(
        cls_name=f'{base_dataclass_.__name__}',
        fields=all_fields,
        bases=(base_dataclass,),
    )

    # Register the new dataclass in the global scope to allow pickling
    globals()[new_dataclass.__name__] = new_dataclass

    # new_dataclass.__module__ = base_dataclass_.__module__
    return new_dataclass


def dataclass_dict_wrapper(dataclass_instance: Any) -> Any:
    """Wrap a dataclass instance to provide dictionary-like access.

    Args:
        dataclass_instance (Any): An instance of a dataclass.

    Example:
        >>> from dataclasses import dataclass
        >>> from pyufunc import dataclass_dict_access
        >>> @dataclass
        ... class Person:
        ...     name: str
        ...     age: int
        >>> person = Person('Alice', 30)
        >>> wrapped_person = dataclass_dict_access(person)
        >>> wrapped_person['name']
        'Alice'
        >>> wrapped_person['age']
        30

    Returns:
        Any: A wrapper object that provides dictionary-like access to the dataclass instance.
    """
    return DataclassDictWrapper(dataclass_instance)


class DataclassDictWrapper:
    """Wrapper class that provides dictionary-like access to a dataclass instance.
    """

    def __init__(self, dataclass_instance):
        if not is_dataclass(dataclass_instance):
            raise ValueError("Provided instance is not a dataclass")
        self._instance = dataclass_instance

    def __getitem__(self, key):
        if hasattr(self._instance, key):
            return getattr(self._instance, key)
        else:
            raise KeyError(f"Key {key} not found in {self._instance.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self._instance, key):
            setattr(self._instance, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self._instance.__class__.__name__}")

    def __getattr__(self, item):
        return getattr(self._instance, item)

    def __setattr__(self, key, value):
        if key == "_instance":
            super().__setattr__(key, value)
        else:
            setattr(self._instance, key, value)
