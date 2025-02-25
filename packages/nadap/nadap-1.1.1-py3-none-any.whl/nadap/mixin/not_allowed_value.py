"""
NotAllowedValueMixin
"""

# pylint: disable=too-few-public-methods

import nadap.schema
from nadap.base import ValEnv, number_to_str_number


class NotAllowedValueMixin:
    """
    Add not allowed value tests for data
    """

    def __init__(self, **kwargs):
        self.not_allowed_values = None
        super().__init__(**kwargs)

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        """
        Check if data doesn't match not allowed values
        """
        data = super()._validate_data(data=data, path=path, env=env)
        if self.not_allowed_values is not None and data in self.not_allowed_values:
            self._create_finding_with_error(
                msg="Data is a not allowed value",
                path=path,
                env=env,
            )
        return data

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        if self.not_allowed_values is not None:
            nadap.schema.is_list(
                self.not_allowed_values, f"{schema_path}.not_allowed_values"
            )
            for index, v in enumerate(self.not_allowed_values):
                self._test_data_type(
                    data=v, path=f"{schema_path}.not_allowed_values[{index}]"
                )

    def _pop_options(self, definition: dict, schema_path: str):
        self.not_allowed_values = definition.pop("not_allowed_values", None)
        super()._pop_options(definition=definition, schema_path=schema_path)

    @property
    def restrictions(self) -> "list[str]":
        """
        Get all restrictions for valid data
        """
        ret_list = super().restrictions
        if self.not_allowed_values:
            ret_list.append("not allowed values:")
            ret_list.extend(
                [f" - {str(number_to_str_number(x))}" for x in self.not_allowed_values]
            )
        return ret_list

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **not_allowed_values** | `list` | | | "
            + " Data mustn't match all of these values |",
            "| &nbsp;&nbsp;- < value > | `any` | | Must match data type's type(s) | |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "not_allowed_values:",
            "  - <any>",
        ]
