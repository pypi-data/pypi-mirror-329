# plateforme.core.types.base
# --------------------------
# Copyright (c) 2023 Plateforme
# This module is part of Plateforme and is released under the MIT License.
# For the full license text, see the LICENSE file at the root directory of the
# project repository or visit https://opensource.org/license/mit.

"""
This module provides utilities for managing base types within the Plateforme
framework leveraging Pydantic schemas for validation and serialization, and
compatibility with SQLAlchemy's data type system.
"""

import typing
from abc import ABCMeta, abstractmethod
from typing import (
    Annotated,
    Any,
    Generic,
    Self,
    TypeVar,
)

from ..database.types import BaseTypeEngine
from ..schema.core import (
    CoreSchema,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
)
from ..schema.json import JsonSchemaDict
from ..schema.types import Strict

_T = TypeVar('_T', bound=Any)

__all__ = (
    'BaseType',
    'BaseTypeFactory',
    'TypeMeta',
)


class TypeMeta(ABCMeta):
    """Metaclass for base type classes."""

    @abstractmethod
    def __get_pydantic_core_schema__(
        cls,
        __source: type[Any],
        __handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Get Pydantic core schema.

        Return the Pydantic core schema for `source` using `handler`. This
        method can be overridden by subclasses to provide a custom core schema.

        Args:
            __source: Source type.
            __handler: Handler function.

        Returns:
            A pydantic core schema.
        """
        # Implement custom logic to generate the core schema...
        ...

    @abstractmethod
    def __get_pydantic_json_schema__(
        cls,
        __core_schema: CoreSchema,
        __handler: GetJsonSchemaHandler,
    ) -> JsonSchemaDict:
        """Get Pydantic JSON schema.

        Return the Pydantic JSON schema for `core_schema` using `handler`. This
        method can be overridden by subclasses to provide a custom JSON schema.

        Args:
            __core_schema: Pydantic core schema.
            __handler: Handler function.

        Returns:
            A modified JSON schema.
        """
        # Implement custom logic to generate the JSON schema...
        ...

    @abstractmethod
    def __get_sqlalchemy_data_type__(
        cls, **kwargs: Any
    ) -> BaseTypeEngine[Any] | None:
        """Get SQLAlchemy data type.

        Return the SQLAlchemy data type engine. This method can be overridden
        by subclasses to provide a custom data type engine.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            A SQLAlchemy target data type engine.
        """
        # Implement custom logic to generate the SQLAlchemy data type engine...
        ...


class BaseTypeFactory(type, Generic[_T]):
    """Base type factory class for Plateforme types."""
    type_: type[_T]

    def __init_subclass__(cls) -> None:
        # Check if class is directly instantiated
        if not hasattr(cls, '__orig_bases__'):
            raise TypeError(
                "Base type factory must be subclassed and not directly "
                "instantiated."
            )
        # Initialize base type
        setattr(cls, 'type_', typing.get_args(cls.__orig_bases__[0])[0])
        return super().__init_subclass__()

    def __new__(
        cls: type['BaseTypeFactory[Any]'],
        /,
        *annotations: Any,
        type_: type[Any] | None = None,
        force_build: bool | None = None,
        strict: bool | None = None,
        **kwargs: Any,
    ) -> type[_T]:
        """Create a new base type with the given annotations.

        Args:
            *annotations: Type annotations to add to the base type class.
            type_: The type to use for the new base type. If not provided, the
                type is inferred from the class definition.
                Defaults to ``None``.
            force_build: Whether to force the build of the base type even if
                the underlying type doesn't inherit from the `BaseType` class.
                Defaults to ``None``.
            strict: Whether to validate the value in strict mode.
                Defaults to ``None``.
            **kwargs: Additional keyword arguments. See below.

        Returns:
            A new base type.

        Note:
            This method is used internally by the Plateforme framework to build
            annotated base types.
        """
        # Validate new type
        if not cls.type_ and not type_:
            raise TypeError(
                "A type must be provided to the base type factory, either "
                "through the `type_` class attribute or the `type_` keyword "
                "argument."
            )
        if cls.type_ and type_ and not issubclass(type_, cls.type_):
            raise TypeError(
                f"The type keyword argument must be a subclass of the factory "
                f"type. Got {type_!r} instead of {cls.type_!r}."
            )
        type_ = type_ or cls.type_

        # Check if new type is a subclass of base type
        if not issubclass(type_, BaseType) and not force_build:
            raise TypeError(
                "Base type factory can only be used with base types when "
                "force build is not enabled."
            )

        # Handle strict annotation
        if strict:
            annotations += \
                (Strict(bool(strict)) if strict is not None else None,)

        return Annotated[  # type: ignore[return-value]
            type_, cls, *annotations
        ]


class BaseType(metaclass=TypeMeta):
    """Base type class for Plateforme types."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Create a new instance of the type."""
        # Check if class is directly instantiated
        if cls is BaseType:
            raise TypeError(
                "Plateforme base type cannot be directly instantiated."
            )
        return super().__new__(cls)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        __source: type[Self],
        __handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return __handler(__source)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        __core_schema: CoreSchema,
        __handler: GetJsonSchemaHandler,
    ) -> JsonSchemaDict:
        return __handler(__core_schema)

    @classmethod
    def __get_sqlalchemy_data_type__(
        cls, **kwargs: Any
    ) -> BaseTypeEngine[Any] | None:
        return None
