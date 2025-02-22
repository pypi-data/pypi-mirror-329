"""
Class Schema
"""

# pylint: disable=too-few-public-methods

import copy
import re
import nadap.types.any
import nadap.types.list
import nadap.types.base
import nadap.types.bool
import nadap.types.bool_false
import nadap.types.bool_true
import nadap.types.enum
import nadap.types.float
import nadap.types.hostname
import nadap.types.idlist
import nadap.types.int
import nadap.types.ip_address
import nadap.types.ip4_address
import nadap.types.ip6_address
import nadap.types.ip_interface
import nadap.types.ip4_interface
import nadap.types.ip6_interface
import nadap.types.ip_network
import nadap.types.ip4_network
import nadap.types.ip6_network
import nadap.types.multitype
import nadap.types.none
import nadap.types.number
import nadap.types.dict
import nadap.types.str
import nadap.references
import nadap.results
from nadap.base import merge_dictionaries, RegexObject
from nadap.errors import SchemaDefinitionError

if hasattr(re, "PatternError"):
    PatternError = re.PatternError
else:
    PatternError = re.error


def is_list(l, path: str):
    """
    Test if given value (t) is a instance of class list; else raise an error.
    """
    if not isinstance(l, list):
        raise SchemaDefinitionError(msg="Must be a list", path=path)


def is_non_empty_list(l, path: str):
    """
    Test if given value (t) is a instance of class list
    and is not empty; else raise an error.
    """
    is_list(l, path)
    if not l:
        raise SchemaDefinitionError(
            msg="Mustn't be empty",
            path=path,
        )


def is_dict(d, path: str):
    """
    Test if given value (d) is a instance of class dict; else raise an error.
    """
    if not isinstance(d, dict):
        raise SchemaDefinitionError(msg="Must be a dictionary", path=path)


def is_str(s, path: str):
    """
    Test if given value (s) is a instance of class str; else raise an error.
    """
    if not isinstance(s, str):
        raise SchemaDefinitionError(msg="Must be a string", path=path)


def is_int(s, path: str):
    """
    Test if given value (s) is a instance of class int; else raise an error.
    """
    if not isinstance(s, int):
        raise SchemaDefinitionError(msg="Must be an integer", path=path)


def no_more_definition_options(definition: dict, source: str, path: str):
    """
    Test if given definition dictionary is empty.
    Else raise an error for containing (unknown) options.
    """
    if definition:
        str_list = list(definition)
        if len(definition) > 1:
            last = str_list[-1]
            str_list = str_list[:-1]
            msg = f"Unknown {source} options {', '.join(str_list)} and {last}"
        else:
            msg = f"Unknown {source} option {str_list[0]}"
        raise SchemaDefinitionError(msg, path)


def compile_regex_string(
    pattern: str, multiline: bool, fullmatch: bool, schema_path: str
) -> "RegexObject":
    """
    Try to compile regex object based on given arguments
    """
    try:
        re_obj = RegexObject(pattern, multiline, fullmatch)
    except (PatternError, TypeError) as e:
        raise SchemaDefinitionError("Not a valid regex pattern", schema_path) from e
    if not pattern:
        raise SchemaDefinitionError(
            "Empty string not allowed as regex pattern", schema_path
        )
    return re_obj


def match_regex_objects(regex_objects: list, data: str) -> tuple[bool, str]:
    """
    Check if string matches any of the regex objects
    """
    for re_obj in regex_objects:
        if re_obj.match(data):
            return True, re_obj.pattern
    return False, ""


class DocTableRow:
    """
    Documentation table entry containing the column values
    """

    header_list = [
        "Variable",
        "Type",
        "Default",
        "Restrictions",
        "Description",
    ]

    def __init__(self, indents: "list[str]", **kwargs):
        self.indents = indents
        self.variable = kwargs.get("variable", "")
        self.type = kwargs.get("type", "")
        self.default = kwargs.get("default", "")
        self.restrictions = kwargs.get("restrictions", [])
        self.description = kwargs.get("description", [])

    def row_value_list(self) -> "list[str]":
        """Get all values within the row as list"""
        return [
            f"{''.join(self.indents)}{self.variable}",
            f"`{self.type}`" if self.type else "",
            self.default,
            self.restrictions,
            self.description,
        ]


class Schema:
    """
    Class Schema
    """

    # pylint: disable=too-many-instance-attributes

    type_class_matching = {
        "any": nadap.types.any.Any,
        "bool": nadap.types.bool.Bool,
        "bool_false": nadap.types.bool_false.BoolFalse,
        "bool_true": nadap.types.bool_true.BoolTrue,
        "dict": nadap.types.dict.Dict,
        "enum": nadap.types.enum.Enum,
        "float": nadap.types.float.Float,
        "hostname": nadap.types.hostname.Hostname,
        "idlist": nadap.types.idlist.IDList,
        "int": nadap.types.int.Int,
        "ip_address": nadap.types.ip_address.IpAddress,
        "ip4_address": nadap.types.ip4_address.Ip4Address,
        "ip6_address": nadap.types.ip6_address.Ip6Address,
        "ip_network": nadap.types.ip_network.IpNetwork,
        "ip4_network": nadap.types.ip4_network.Ip4Network,
        "ip6_network": nadap.types.ip6_network.Ip6Network,
        "ip_interface": nadap.types.ip_interface.IpInterface,
        "ip4_interface": nadap.types.ip4_interface.Ip4Interface,
        "ip6_interface": nadap.types.ip6_interface.Ip6Interface,
        "list": nadap.types.list.List,
        "multitype": nadap.types.multitype.MultiType,
        "none": nadap.types.none.Null,
        "number": nadap.types.number.Number,
        "str": nadap.types.str.Str,
    }

    def __init__(self, definition: dict = None):
        self.references = nadap.references.References()
        self.reference_findings = []

        self.name = ""
        self.description = ""

        self.root = None
        self.custom_data_types = {}
        self.templates = {}
        self.template_merge_recursive = False
        self.template_list_merge = "append_rp"
        self.template_stack = []

        if definition is not None:
            self.load_definition(definition)

    def _is_loaded(self):
        """
        Check if Schema has loaded a schema definition
        """
        if self.root is None:
            raise RuntimeError("Schema definition hasn't been loaded")

    def _merge_template_definition(self, definition: dict, path: str) -> dict:
        definition = copy.deepcopy(definition)
        template_name = definition.pop("template", None)
        if template_name:
            if f"template.{template_name}" in path.split(" > "):
                raise SchemaDefinitionError(
                    "Nested template loop", f"{path} > template.{template_name}"
                )
            if template_name not in self.templates:
                raise SchemaDefinitionError(
                    f"Unknown template {template_name}",
                    f"{path}.template",
                )
            t_merge_opts = definition.pop("template_merge_options", {})
            definition = merge_dictionaries(
                left=self.templates[template_name],
                right=definition,
                recursive=t_merge_opts.pop("recursive", self.template_merge_recursive),
                list_merge=t_merge_opts.pop("list_merge", self.template_list_merge),
            )
            definition = self._merge_template_definition(
                definition, f"{path} > template.{template_name}"
            )
        return definition

    def load_data_type_by_definition(
        self, definition: dict | str, path: str
    ) -> nadap.types.base.BaseType:
        """
        Identify and load data type object by given definition.
        """
        if isinstance(definition, str):
            definition = {"type": definition}
        elif not isinstance(definition, dict):
            raise SchemaDefinitionError(
                "Data type definition must be a string or dictionary", path
            )
        # First look up if this is an custom data type:
        if cdt_def := self.custom_data_types.get(definition.get("type", None), None):
            new_def = copy.deepcopy(cdt_def)
            new_def.update(definition)
            definition = new_def
        if template_name := definition.pop("template", None):
            if template_name not in self.templates:
                raise SchemaDefinitionError(
                    f"Unknown template {template_name}",
                    f"{path}.template",
                )
            t_merge_opts = definition.pop("template_merge_options", {})
            definition = merge_dictionaries(
                left=self.templates[template_name],
                right=definition,
                recursive=t_merge_opts.pop("recursive", self.template_merge_recursive),
                list_merge=t_merge_opts.pop("list_merge", self.template_list_merge),
            )
        _type = definition.pop("type", None)
        if _type is None:
            raise SchemaDefinitionError(msg="Key 'type' missing.", path=path)
        # If this is a CDT options have already been merged,
        # but "type" was overwritten. Pull in "type" excplicitly from CDT.
        if _type in self.custom_data_types:
            _type = self.custom_data_types[_type]["type"]
        if _type not in self.type_class_matching:
            raise SchemaDefinitionError(
                msg=f"Data type '{_type}' not found",
                path=path,
            )
        data_type_class = self.type_class_matching[_type]
        data_type = data_type_class(
            schema=self, definition=definition, schema_path=path
        )
        if unknown_options := sorted(definition):
            if len(unknown_options) > 1:
                unknown_options = [f"'{x}'" for x in unknown_options]
                msg = f"Unknown options {', '.join(unknown_options)}"
            else:
                msg = f"Unknown option '{unknown_options[0]}'"
            raise SchemaDefinitionError(
                msg=f"{msg} for data type {data_type_class.data_type_name}", path=path
            )
        return data_type

    def _parse_custom_data_types(self, definition):
        for name, cdt_definition in definition.pop("custom_data_types", {}).items():
            if cdt_definition.get("type", None) not in self.type_class_matching:
                raise SchemaDefinitionError(
                    "Not a built-in data type", f"custom_data_types.{name}"
                )
            self.load_data_type_by_definition(
                copy.deepcopy(cdt_definition),
                f"custom_data_types.{name}",
            )
            self.custom_data_types[name] = cdt_definition

    def _parse_templates(self, definition):
        self.templates = definition.pop("templates", {})
        # Check if template definition is a correct data type definition.
        for name, t_definition in self.templates.items():
            self.templates[name] = self._merge_template_definition(
                t_definition, f"template.{name}"
            )

    def load_definition(self, definition: dict) -> "nadap.types.base.DataType":
        """
        Parse schema definition and returns the root data type of this schema.
        """
        definition = copy.deepcopy(definition)
        self.name = definition.pop("name", "")
        self.description = definition.pop("description", "")
        self._parse_templates(definition)
        self._parse_custom_data_types(definition)
        try:
            root = definition.pop("root")
        except KeyError as e:
            raise SchemaDefinitionError(f"Missing schema definition key {e}") from e
        if unknown_options := sorted(definition):
            if len(unknown_options) > 1:
                unknown_options = [f"'{x}'" for x in unknown_options]
                msg = f"Unknown schema options {', '.join(unknown_options)}"
            else:
                msg = f"Unknown schema option '{unknown_options[0]}'"
            raise SchemaDefinitionError(msg=msg)
        self.root = self.load_data_type_by_definition(
            definition=root,
            path="root",
        )
        return self.root

    @property
    def _markdown_header(self) -> str:
        return (
            f"| { ' | '.join(f'**{x}**' for x in DocTableRow.header_list)} |\n"
            + f"{'| --- ' * len(DocTableRow.header_list)} |\n"
        )

    def _render_markdown_table(self, rows: "list[DocTableRow]") -> str:
        table_str = self._markdown_header
        table_rows = []
        for e in rows:
            v, t, _def, r, des = e.row_value_list()
            r = r"<br>".join(r)
            des = r"<br>".join(des)
            table_rows.append(f"| {' | '.join([v, t, _def, r, des])} |")
        return table_str + "\n".join(table_rows)

    def _render_yaml_table(self, rows: "list[DocTableRow]") -> str:
        table_str = self._markdown_header
        for e in rows:
            v, t, _def, r, des = e.row_value_list()
            if isinstance(des, list):
                des = "<br>".join(des)
            table_str += f"| {' | '.join([v, t, _def, '<br>'.join(r), des])} |\n"
        return table_str

    @property
    def _doc_markdown_table(self):
        rows = self.root.markdown_table_rows
        if (
            len(rows) > 1
            and set(self.root.python_classes) == {dict}
            and not rows[0].default
            and not rows[0].description
        ):
            rows = rows[1:]
        return rows

    def doc(self, fmt: str) -> str:
        """
        Get documentation for this data schema

        Arguments:
            format:     str
                        Intended output format
                        Allowed values:
                        - markdown
                        - yaml
        Returns:        str
                        Documentation in requested format
        """
        self._is_loaded()

        if fmt == "markdown":
            ret_str = self._render_markdown_table(self._doc_markdown_table)
        elif fmt == "yaml":
            ret_str = "\n".join(self.root.doc_yaml)
        else:
            raise RuntimeError("Unknown documentation format")
        return ret_str

    def _get_level_markdown_dict(
        self,
        rows: list[DocTableRow],
        level: int,
        path_rows: list[DocTableRow] = None,
    ) -> dict:
        # pylint: disable=too-many-return-statements
        if not path_rows:
            path_rows = []
            path = ""
        else:
            path = ".".join([row.variable for row in path_rows[1:]])
        if not rows:
            if len(path_rows) > 1 and path_rows[-1].type == "dict":
                return {path: path_rows[1:]}
            return {}
        first_row = rows[0]
        if len(first_row.indents) > level:
            return {path: path_rows[1:] + rows}
        ret_dict = {}
        if not path_rows:
            # len(indents) == 0 ==> root data type
            if first_row.type != "dict":  # Anything else than a dict
                ret_dict["__root__"] = rows
                return {"__root__": rows}
            return self._get_level_markdown_dict(rows[1:], level, [first_row])
        if first_row.type != "dict":  # Anything else than a dict
            ret_dict[f"{path}.{first_row.variable}" if path else first_row.variable] = (
                path_rows[1:] + [first_row]
            )
            ret_dict.update(self._get_level_markdown_dict(rows[1:], level, path_rows))
            return ret_dict

        sub_rows = []
        for row in rows[1:]:
            if len(row.indents) > len(first_row.indents):
                # Table row is a sub row
                sub_rows.append(row)
        ret_dict.update(
            self._get_level_markdown_dict(sub_rows, level, path_rows + [first_row])
        )
        if len(rows) > len(sub_rows) + 1:
            remaining_rows = rows[len(sub_rows) + 1 :]
            ret_dict.update(
                self._get_level_markdown_dict(remaining_rows, level, path_rows)
            )

        return ret_dict

    def _get_level_yaml_dict(
        self,
        rows: list[str],
        level: int,
        path_rows: list[str] = None,
    ) -> dict:
        # pylint: disable=too-many-return-statements,too-many-branches
        def _get_indent(s: str, i: int = 0) -> int:
            if len(s) > 1 and s[:2] == "  ":
                return _get_indent(s[2:], i + 1)
            return i

        if not rows:
            return {}
        if not path_rows:
            path_rows = []
            path = ""
        else:
            path = ".".join([row.split(":")[0].strip() for row in path_rows])

        # This iteration is too deep, just create the dictionary entry with current rows
        if len(path_rows) > level:
            return {path: path_rows + rows}

        ret_dict = {}
        first_row = rows[0]
        if first_row.endswith(":"):
            # dictionary with nested structure
            sub_rows = []
            for row in rows[1:]:
                if _get_indent(row) > _get_indent(first_row):
                    sub_rows.append(row)
                else:
                    break
            ret_dict.update(
                self._get_level_yaml_dict(sub_rows, level, path_rows + [first_row])
            )
            ret_dict.update(
                self._get_level_yaml_dict(rows[len(sub_rows) + 1 :], level, path_rows)
            )
        elif ":" in first_row:
            # This is  key value pair
            # Add this row to the dictionary
            if path:
                ret_dict[f"{path}.{first_row.split(':')[0].strip()}"] = path_rows + [
                    first_row
                ]
            else:
                ret_dict[first_row.split(":")[0]] = [first_row]
            # And iterate on remaining rows again
            ret_dict.update(self._get_level_yaml_dict(rows[1:], level, path_rows))
        else:
            # This is something else; not a dict or key
            if path:
                ret_dict[path] = path_rows + rows
            else:
                ret_dict["__root__"] = rows

        return ret_dict

    def doc_sections(self, fmt: str, level: int = 0) -> dict:
        """
        Get documentation split into sections.
        If data type is an object data type, documentation is
        split into each key. This is done recursively up to 'level' deep.

        Arguments:
            format:     str
                        Intended output format
                        Allowed values:
                        - markdown
                        - yaml
            level:      int >= 0
                        Split level
        Returns:        dict
                        Keys: keys in data type
                        Values:
                            str - Key path within data schema
                            str - Documentation of sub data schema
        """
        # Check if schema is initialized
        self._is_loaded()

        # Parse split rows to intended format
        dict_str = {}
        if fmt == "markdown":
            # Get all doc table rows
            rows = self.root.markdown_table_rows
            # Split rows into data path levels
            dict_list = self._get_level_markdown_dict(rows, level)
            for data_path, rows in dict_list.items():
                dict_str[data_path] = self._render_markdown_table(rows)
        else:
            yaml_doc = self.root.doc_yaml
            dict_list = self._get_level_yaml_dict(yaml_doc, level)
            for data_path, rows in dict_list.items():
                dict_str[data_path] = "\n".join(rows)
        return dict_str
