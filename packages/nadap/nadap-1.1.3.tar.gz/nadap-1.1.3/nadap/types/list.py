"""
List classes
"""

# pylint: disable=too-few-public-methods

import nadap.results
import nadap.types.base
import nadap.mixin.replace_empty_to
import nadap.mixin.min_max
import nadap.schema
from nadap.base import ValEnv
from nadap.errors import DataValidationError

DOC_DT_NAME = "List"
DOC_DT_DESCRIPTION = """
An **list** data type tests data for being an instance of
python's built-in class `list`.
"""
DOC_DT_FEATURES = """
- Validate list length
- Validate uniqueness of elements
- Supports **Referencing Feature**
"""
DOC_DT_YAML_EXAMPLE = """
type: list
description: "Example list definition for a list of strings"
default_value:
  - nadap
  - rulez!

minimum: 2
maximum: 15
allow_duplicates: false

elements: str

reference: ref_key
"""


class ListBase(
    nadap.mixin.replace_empty_to.ReplaceEmptyToMixin,
    nadap.mixin.min_max.MinMaxLengthMixin,
    nadap.types.base.BaseType,
):
    """
    List datatype base class
    """

    _cls_python_classes = [list]
    _support_replace_empty_to = True

    def __init__(self, **kwargs):
        self.elements_data_type = None
        super().__init__(**kwargs)

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        self.elements_data_type = self._schema.load_data_type_by_definition(
            self.elements_data_type, f"{schema_path}.elements"
        )

    def _pop_options(self, definition: dict, schema_path: str):
        self.elements_data_type = definition.pop("elements", "any")
        super()._pop_options(definition, schema_path)

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **elements** | <code>dict&#124;str</code> | | required | "
            + "List element's data type definition |",
            "| &nbsp;&nbsp;*option 1* | `str` | | "
            + "List element's data type string (short definition) |",
            "| &nbsp;&nbsp;*option 2* | `dict` | | "
            + "List element's data type definition |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "",
            "elements: <dict|str>",
            "  # Mulitype!!!",
            "  <str>",
            "  # or",
            "  <dict>",
        ]


class List(ListBase):
    """
    List datatype class
    """

    data_type_name = "list"
    _doc_data_type = "list"

    def __init__(self, **kwargs):
        self.allow_duplicates = True
        super().__init__(**kwargs)

    def _pop_options(self, definition: dict, schema_path: str):
        self.allow_duplicates = definition.pop("allow_duplicates", True)
        super()._pop_options(definition, schema_path)

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        data = super()._validate_data(data=data, path=path, env=env)
        ret_data = []
        invalid = False
        processed_elements = []
        for index, v in enumerate(data):
            if not self.allow_duplicates and v in processed_elements:
                env.findings.append(
                    nadap.results.ValidationFinding(
                        "Duplicate list element", f"{path}[{index}]"
                    )
                )
                invalid = True
            else:
                try:
                    e_data = self.elements_data_type.validate(
                        data=v,
                        path=f"{path}[{index}]",
                        env=env,
                    )
                except DataValidationError:
                    invalid = True
                else:
                    ret_data.append(e_data)
                    processed_elements.append(e_data)
        if invalid:
            raise DataValidationError
        return ret_data

    @property
    def doc_data_type(self) -> str:
        """Get markdown data type string"""
        if self.elements_data_type.doc_python_classes:
            return f"list[{self.elements_data_type.doc_python_classes}]"
        return f"list[{self.elements_data_type.data_type_name}]"

    @property
    def markdown_table_rows(self) -> "list[nadap.schema.DocTableRow]":
        """
        Get markdown table rows for this data type definition
        """
        e_rows = self.elements_data_type.markdown_table_rows
        if len(e_rows) == 1:
            # Element is not a data structure
            e_rows[0].variable = f"< {self.elements_data_type.doc_value_name} >"
        elif e_rows[0].type.startswith("list"):
            # Element is a list
            for row in e_rows[1:]:
                row.indents.insert(0, self._markdown_indent)
        else:
            # Element is a non-empty dictionary
            e_rows = e_rows[1:]
            for row in e_rows[1:]:
                row.indents.insert(0, self._markdown_indent)

        e_rows[0].indents.insert(0, "- ")
        return super().markdown_table_rows + e_rows

    @property
    def doc_yaml(self) -> "list[str]":
        """
        Get data structure
        """
        element_doc_yaml = self.elements_data_type.doc_yaml
        ret_lines = []
        for index, line in enumerate(element_doc_yaml):
            if not index:
                ret_lines.append(f"- {line}")
                continue
            ret_lines.append(f"  {line}")
        return ret_lines

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **allow_duplicates** | `bool` | true | | |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "allow_duplicates: <true|false>",
        ]


DOC_DT_CLASS = List  # pylint: disable=invalid-name
