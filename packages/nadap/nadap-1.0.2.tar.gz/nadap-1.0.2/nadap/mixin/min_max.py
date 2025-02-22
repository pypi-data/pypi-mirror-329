"""
MinMaxLengthMixin
"""

# pylint: disable=too-few-public-methods

from nadap.errors import SchemaDefinitionError
from nadap.base import ValEnv


class _PopOptionsMixin:
    """
    Mixin for popping the options
    """

    def _pop_options(self, definition: dict, schema_path: str):
        self.maximum = definition.pop("maximum", None)
        self.minimum = definition.pop("minimum", None)
        super()._pop_options(definition=definition, schema_path=schema_path)


class MinMaxValueMixin(_PopOptionsMixin):
    """
    Add min/max tests for value data
    """

    def __init__(self, **kwargs):
        self.minimum = None
        self.maximum = None
        super().__init__(**kwargs)

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        """
        Check if data matches defined data type and apply preprocessing
        """
        data = super()._validate_data(data=data, path=path, env=env)
        if self.minimum is not None and data < self.minimum:
            self._create_finding_with_error(
                msg=f"Value is lower than defined minimum of {self.minimum}",
                path=path,
                env=env,
            )
        if self.maximum is not None and data > self.maximum:
            self._create_finding_with_error(
                msg=f"Value is greater than defined maximum of {self.maximum}",
                path=path,
                env=env,
            )
        return data

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        if self.maximum is not None and not isinstance(
            self.maximum, tuple(self.python_classes)
        ):
            raise SchemaDefinitionError(
                self._data_type_mismatch_message,
                f"{schema_path}.maximum",
            )
        if self.minimum is not None:
            if not isinstance(self.minimum, tuple(self.python_classes)):
                raise SchemaDefinitionError(
                    self._data_type_mismatch_message,
                    f"{schema_path}.minimum",
                )
        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise SchemaDefinitionError(
                "maximum must be greater than or equal to minimum",
                schema_path,
            )

    @property
    def restrictions(self) -> "list[str]":
        """
        Get all restrictions for valid data
        """
        ret_list = super().restrictions
        if self.minimum is not None:
            ret_list.append(f"min: {self.minimum}")
        if self.maximum is not None:
            ret_list.append(f"max: {self.maximum}")
        return ret_list

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **minimum** | <code>"
            + "&#124;".join(sorted([x.__name__ for x in cls._cls_python_classes]))
            + "</code> | | |  Value must be greater or equal |",
            "| **maximum** | <code>"
            + "&#124;".join(sorted([x.__name__ for x in cls._cls_python_classes]))
            + "</code> | | >= 'minimum' |  Value must be lower or equal |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            f"maximum: <{'|'.join(sorted([x.__name__ for x in cls._cls_python_classes]))}>",
            f"minimum: <{'|'.join(sorted([x.__name__ for x in cls._cls_python_classes]))}>",
        ]


class MinMaxLengthMixin(_PopOptionsMixin):
    """
    Add min/max tests for value data length
    """

    def __init__(self, **kwargs):
        self.minimum = None
        self.maximum = None
        super().__init__(**kwargs)

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        """
        Check if data matches defined data type and apply preprocessing
        """
        data = super()._validate_data(data=data, path=path, env=env)
        if self.minimum is not None and len(data) < self.minimum:
            self._create_finding_with_error(
                msg=f"Length is lower than defined minimum of {self.minimum}",
                path=path,
                env=env,
            )
        if self.maximum is not None and len(data) > self.maximum:
            self._create_finding_with_error(
                msg=f"Length is greater than defined maximum of {self.maximum}",
                path=path,
                env=env,
            )
        return data

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        if self.maximum is not None:
            if not isinstance(self.maximum, int):
                raise SchemaDefinitionError(
                    "Data is not an instance of 'int'",
                    f"{schema_path}.maximum",
                )
            if self.maximum < 0:
                raise SchemaDefinitionError(
                    "Must be >= 0",
                    f"{schema_path}.maximum",
                )
        if self.minimum is not None:
            if not isinstance(self.minimum, int):
                raise SchemaDefinitionError(
                    "Data is not an instance of 'int'",
                    f"{schema_path}.minimum",
                )
            if self.minimum < 0:
                raise SchemaDefinitionError(
                    "Must be >= 0",
                    f"{schema_path}.minimum",
                )
        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise SchemaDefinitionError(
                "maximum must be greater than or equal to minimum",
                schema_path,
            )

    @property
    def restrictions(self) -> "list[str]":
        """
        Get all restrictions for valid data
        """
        ret_list = super().restrictions
        if self.minimum is not None:
            ret_list.append(f"min length: {self.minimum}")
        if self.maximum is not None:
            ret_list.append(f"max length: {self.maximum}")
        return ret_list

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **minimum** | `int` | | min: 1 | Data's length must be greater or equal |",
            "| **maximum** | `int` | | min: 1<br>>= 'minimum' | "
            + "Data's length must be lower or equal |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "maximum: <int>",
            "minimum: <int>",
        ]
