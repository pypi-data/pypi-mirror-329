"""
ID list class
"""

# pylint: disable=too-few-public-methods

import nadap.results
import nadap.types.base
import nadap.types.list
import nadap.schema
from nadap.base import ValEnv
from nadap.errors import DataValidationError

DOC_DT_NAME = "IDList"
DOC_DT_DESCRIPTION = """
An **idlist** data type represents a python dictionary with IDs as keys.
It tests data for being an instance of python's built-in class `dict`.
"""
DOC_DT_FEATURES = """
- Validate number of IDs/keys
- Validate IDs/keys with nested data type definition
- Supports **Referencing Feature**
"""
DOC_DT_YAML_EXAMPLE = """
type: idlist
description: |
  Example idlist definition for string IDs with integer values and
  enhanced referencing.
default_value:
  nadap: 1
  rulez!: 2

minimum: 2
maximum: 15

id:
  type: str
  reference: ref_key_id
elements:
  type: int
  reference: ref_key_element
"""


class IDList(
    nadap.types.list.ListBase,
):
    """
    ID list datatype class (dictionary with IDs as keys)
    """

    data_type_name = "idlist"
    _cls_python_classes = [dict]
    _doc_data_type = "dict"

    def __init__(self, **kwargs):
        self.id_data_type = None
        super().__init__(**kwargs)

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        self.id_data_type = self._schema.load_data_type_by_definition(
            self.id_data_type, f"{schema_path}.id"
        )

    def _pop_options(self, definition: dict, schema_path: str):
        self.id_data_type = definition.pop("id", "str")
        super()._pop_options(definition, schema_path)

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        data = super()._validate_data(data=data, path=path, env=env)
        ret_dict = {}
        for index, k in enumerate(data):
            try:
                r_key = self.id_data_type.validate(
                    data=k,
                    path=f"{path}{{#{index}}}",
                    env=env,
                )
                r_data = self.elements_data_type.validate(
                    data=data[k],
                    path=f"{path}.{k}",
                    env=env,
                )
            except DataValidationError:
                ret_dict = None
            else:
                if ret_dict is not None:
                    ret_dict[r_key] = r_data
        if ret_dict is None:
            raise DataValidationError()
        return ret_dict

    @property
    def markdown_table_rows(self) -> "list[nadap.schema.DocTableRow]":
        """
        Get markdown table rows for this data type definition
        """
        ret_list = super().markdown_table_rows

        id_e_rows = self.elements_data_type.markdown_table_rows
        if (
            len(id_e_rows) > 1
            and set(self.elements_data_type.python_classes) == {dict}
            and not id_e_rows[0].default
            and not id_e_rows[0].description
        ):
            id_e_rows = id_e_rows[1:]
        for row in id_e_rows:
            row.indents.insert(0, self._markdown_indent)

        id_rows = self.id_data_type.markdown_table_rows
        if not set(self.elements_data_type.python_classes).intersection({dict, list}):
            # id row and value info needs to be merged.
            id_rows[0].type = id_e_rows[0].type
            id_rows[0].variable = f"< {self.id_data_type.doc_data_type} >"
            id_rows[0].default = id_e_rows[0].default
            if id_rows[0].restrictions:
                id_rows[0].restrictions = ["Variable:"] + [
                    f"&nbsp;&nbsp;{x}" for x in id_rows[0].restrictions
                ]
            if id_e_rows[0].restrictions:
                id_rows[0].restrictions.extend(
                    ["Value:"] + [f"&nbsp;&nbsp;{x}" for x in id_e_rows[0].restrictions]
                )
            if id_rows[0].description:
                id_rows[0].description = ["Variable:"] + [
                    f"&nbsp;&nbsp;{x}" for x in id_rows[0].description
                ]
            if id_e_rows[0].description:
                id_rows[0].description.extend(
                    ["Value:"] + [f"&nbsp;&nbsp;{x}" for x in id_e_rows[0].description]
                )
            return ret_list + id_rows

        id_rows[0].type = ""
        id_rows[0].variable = f"< {self.id_data_type.doc_data_type} >"
        return ret_list + id_rows + id_e_rows

    @property
    def doc_yaml(self) -> "list[str]":
        """
        Get data structure
        """
        if (
            dict in self.elements_data_type.python_classes
            or list in self.elements_data_type.python_classes
        ):
            return [f"<{self.id_data_type.doc_data_type}>:"] + [
                f"  {x}" for x in self.elements_data_type.doc_yaml
            ]
        return [
            f"<{self.id_data_type.doc_data_type}>: {self.elements_data_type.doc_yaml[0]}"
        ]

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **id** | <code>dict&#124;str</code> | | | "
            + "ID's data type definition |",
            "| &nbsp;&nbsp;*option 1* | `str` | 'str' | "
            + "ID's data type string (short definition) |",
            "| &nbsp;&nbsp;*option 2* | `dict` | | ID's data type definition |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "",
            "id: <dict|str>",
            "  # Mulitype!!!",
            "  <str>",
            "  # or",
            "  <dict>",
        ]


DOC_DT_CLASS = IDList  # pylint: disable=invalid-name
