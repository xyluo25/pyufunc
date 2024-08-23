'''
##############################################################
# Created Date: Thursday, August 22nd 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

from dataclasses import dataclass, field, fields, make_dataclass, MISSING, is_dataclass
from typing import Any, List, Tuple, Type, Union


def create_dataclass(class_name: str, attributes: List[Union[Tuple[str, Type, Any], Tuple[str, Any]]]) -> Type:
    """
    Dynamically creates a dataclass with the given attributes.

    Args:
        class_name (str): The name of the dataclass to create.
        attributes (List[Union[Tuple[str, Type, Any], Tuple[str, Any]]]):
            A list of tuples where each tuple can be:
            - (attribute_name, type, default_value): The attribute name, type, and a default value.
            - (attribute_name, default_value): The attribute name and a default value, with the type inferred.

    Returns:
        Type: A new dataclass with the specified attributes.

    Example:
        >>> attributes = [
        ...     ('attribute_one', int, 10),
        ...     ('attribute_two', "default_value"),  # Type inferred as str
        ...     ('attribute_three', float, 0.0)
        ... ]
        >>> DynamicClass = create_dataclass('DynamicClass', attributes)
        >>> instance = DynamicClass(attribute_one=1)
        >>> print(instance.attribute_one)
        1
        >>> print(instance.attribute_two)
        default_value
        >>> print(instance.attribute_three)
        0.0
    """
    processed_attributes = []

    for attr in attributes:
        if len(attr) == 2:
            # Name and default value provided, type is inferred
            processed_attributes.append((attr[0], type(attr[1]), attr[1]))
        elif len(attr) == 3:
            # Name, type, and default value provided
            processed_attributes.append((attr[0], attr[1], attr[2]))

    return make_dataclass(class_name, processed_attributes)


def merge_dataclass(dataclass_one: Type[Any], dataclass_two: Type[Any],
                    prefer: str = 'first',
                    *,
                    merged_class_name: str = "") -> Type[Any]:
    """Merges two dataclasses into a single new dataclass, handling duplicate attributes.

    Args:
        dataclass_one (Type[Any]): The first dataclass to merge.
        dataclass_two (Type[Any]): The second dataclass to merge.
        prefer (str, optional): Specifies which dataclass to prefer in case of duplicate attributes.
            Defaults to 'first':
                - (option): 'first'
                - (option): 'second'

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


def extend_dataclass(
    base_dataclass: Type[Any],
    additional_attributes: List[Tuple[str, Type[Any], Any]]
) -> Type[Any]:
    """Creates a new dataclass by extending the base_dataclass with additional_attributes.

    Args:
        base_dataclass (dataclass): The base dataclass to extend.
        additional_attributes (list): A list of tuples in the form (name, type, default_value).
            or (name, default_value) to add to the base dataclass.

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

    # Extract existing fields from the base dataclass
    base_fields = []
    for f in fields(base_dataclass):
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

    return make_dataclass(
        cls_name=f'{base_dataclass.__name__}',
        fields=all_fields,
        bases=(base_dataclass,),
    )
