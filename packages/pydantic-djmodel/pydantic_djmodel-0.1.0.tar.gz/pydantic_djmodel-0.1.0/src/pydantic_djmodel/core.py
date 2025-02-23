"""Main module."""

import re
import sys

from pathlib import Path
from typing import Union, get_args, get_origin

import django

from django.db import models
from pydantic import BaseModel

# settings.configure(default_settings="seconddx.settings", DEBUG=True)
django.setup()

secondddx_path = Path('.').absolute().parent
sys.path.insert(0, str(secondddx_path))


def camel_to_snake(name: str) -> str:
    """
    Convert a camelCase or PascalCase string to snake_case.

    Parameters
    ----------
    name : str
        The string to convert.

    Returns
    -------
    str
        The converted string.

    Notes
    -----
    This function is not idempotent. If the input string is already in
    snake_case, running it through this function will make it lower case.

    Examples
    --------
    >>> camel_to_snake("camelCaseExample")
    "camel_case_example"
    >>> camel_to_snake("PascalCaseExample")
    "pascal_case_example"
    """
    name = re.sub(  # pyright: ignore[reportGeneralTypeIssues]
        r'(?<!^)(?=[A-Z])', '_', name
    )  # Insert _ before uppercase letters (excluding the first)
    return name.lower()


def pydantic_to_django(
    pydantic_model: BaseModel, model_name: str, module_name: str = 'seconddx'
) -> type:
    """
    Dynamically generates a Django model class from a Pydantic model.

    Parameters
    ----------
    pydantic_model : BaseModel
        The Pydantic model to generate a Django model from.
    model_name : str
        The name to give the generated Django model class.
    module_name : str, optional
        The module name to use for the generated Django model.
        Defaults to 'seconddx'.

    Returns
    -------
    type
        The generated Django model class.
    """
    fields = {}

    for field_name, field_info in pydantic_model.model_fields.items():
        field_type = field_info.annotation

        field_name = camel_to_snake(field_name)

        # Handle Union types (Optional fields)
        if get_origin(field_type) is Union:
            field_type = get_args(field_type)[0]  # Take the first valid type

        # Map Pydantic types to Django ORM fields
        if field_type is str:
            fields[field_name] = models.CharField(
                max_length=255, blank=True, null=True
            )
        elif field_type is int:
            fields[field_name] = models.IntegerField(blank=True, null=True)
        elif field_type is float:
            fields[field_name] = models.FloatField(blank=True, null=True)
        elif field_type is bool:
            fields[field_name] = models.BooleanField(default=False)
        elif get_origin(field_type) is list:
            fields[field_name] = models.JSONField(
                blank=True, null=True
            )  # Lists stored as JSON
        else:
            fields[field_name] = models.JSONField(
                blank=True, null=True
            )  # Default to JSONField for unknown types

    # Add common FHIR fields
    # fields["fhir_id"] = models.CharField(
    # max_length=64, unique=True, blank=True, null=True)
    # fields["image"] = models.ImageField(upload_to=f"{
    # model_name.lower()}s/", blank=True, null=True)
    # fields["original_language"] = models.CharField(
    # max_length=10, blank=True, null=True)

    # Ensure Django recognizes the generated model
    fields['__module__'] = module_name

    # Create Django model dynamically
    return type(model_name, (models.Model,), fields)
