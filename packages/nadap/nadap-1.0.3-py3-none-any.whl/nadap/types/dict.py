"""
Dict class
"""

# pylint: disable=too-few-public-methods

from collections import OrderedDict
import copy
import nadap.results
import nadap.types.base
import nadap.mixin.regex_mode
import nadap.mixin.replace_empty_to
import nadap.schema
from nadap.base import UNDEFINED, number_to_str_number, ValEnv
from nadap.errors import SchemaDefinitionError, DataValidationError

DOC_DT_NAME = "Dictionary"
DOC_DT_DESCRIPTION = """
A **dict** data type tests data for being an instance of
python's built-in class `dict`.
"""
DOC_DT_FEATURES = """
- Check data type of key values.
- **Regex Mode** matches keys based on regex patterns.
- Advanced data key validation:
  - Check data for **required** keys
  - Validate **restrictions** among data keys like *requires*, *excludes* or *xor*
- Supports **Referencing Feature**. Adds an option to filter key/value pairs used as reference value
"""
DOC_DT_YAML_EXAMPLE = """
type: dict
description: "Example dict definition with regex mode enabled and some key restrictions in place"
default_value:
  a11: 1
reference:
references:
  - 'unique_key'
  - key: 'consumer_key'
    mode: consumer
    keys:
      - b11  # If key b11 is in data it is included in reference data
      - 12  # If key 12 is in data it is included in reference data

keys:
  11: str
  a11: int
  a12: int
  12: str
  b11: float
  b12: float

restrictions:
  keys:
    b11:
      requires:
        - a11  # If key b11 in data key a11 must be in data, too
      excludes:
        - b12  # If key b11 in data key b12 mustn't be in data
  required:
    - a11  # Key 'a11' must be in data
  xor_required:
    -  # If key 11 is in data key 12 mustn't be in data - and vice-versa
      - 11
      - 11
"""


class Dict(
    nadap.mixin.replace_empty_to.ReplaceEmptyToMixin,
    nadap.mixin.regex_mode.RegexModeMixin,
    nadap.types.base.BaseType,
):
    """
    Dict datatype class
    """

    data_type_name = "dict"
    _cls_python_classes = [dict]
    _support_replace_empty_to = True
    _doc_data_type = "dict"

    def __init__(self, **kwargs):
        self.keys = None
        self.regex_store = {}
        self.key_restrictions = {}
        self.required_keys = []
        self.xor_required = []
        self.ignore_unknown_keys = False
        self.reference_keys = []
        super().__init__(**kwargs)

    def _check_for_defined_key(self, a_name: any, schema_path: str):
        if not self.regex_mode and a_name not in self.keys:
            raise SchemaDefinitionError("Key not defined", schema_path)

    def _key_regex(self, a_name: str, schema_path: str):
        if self.regex_mode:
            self.regex_store[a_name] = nadap.schema.compile_regex_string(
                pattern=a_name,
                multiline=self.regex_multiline,
                fullmatch=self.regex_fullmatch,
                schema_path=schema_path,
            )

    def _validate_keys_option(self, schema_path: str):
        if not self.keys:
            return
        nadap.schema.is_dict(self.keys, schema_path)
        keys_definition = self.keys
        self.keys = OrderedDict()
        for a_name, a_definition in keys_definition.items():
            a_path = f"{schema_path}.{a_name}"
            self._key_regex(a_name, a_path)
            self.keys[a_name] = self._schema.load_data_type_by_definition(
                definition=a_definition, path=a_path
            )

    def _parse_key_restrictions(self, restrictions: dict, schema_path: str):
        nadap.schema.is_dict(restrictions, schema_path)
        restrictions = copy.deepcopy(restrictions)
        requires = restrictions.pop("requires", [])
        req_path = f"{schema_path}.requires"
        nadap.schema.is_list(requires, req_path)
        for index, a_name in enumerate(requires):
            _path = f"{req_path}[{index}]"
            self._check_for_defined_key(a_name, _path)
            self._key_regex(a_name, _path)
        excludes = restrictions.pop("excludes", [])
        ex_path = f"{schema_path}.excludes"
        nadap.schema.is_list(excludes, ex_path)
        for index, a_name in enumerate(excludes):
            _path = f"{ex_path}[{index}]"
            self._check_for_defined_key(a_name, _path)
            self._key_regex(a_name, _path)
        nadap.schema.no_more_definition_options(
            definition=restrictions,
            source="key restrictions",
            path=schema_path,
        )

    def _validate_restrictions_option(self, schema_path: str):
        if not self.key_restrictions:
            return
        if not self.keys:
            raise SchemaDefinitionError(
                "Not allowed if no keys are defined",
                f"{schema_path}.restrictions",
            )
        nadap.schema.is_dict(self.key_restrictions, schema_path)
        restrictions = self.key_restrictions
        # Parse required_keys:
        req_attr = restrictions.pop("required", [])
        if req_attr == "all":
            self.required_keys = list(self.keys)
        else:
            nadap.schema.is_list(req_attr, f"{schema_path}.required")
            for index, a_name in enumerate(req_attr):
                _path = f"{schema_path}.required[{index}]"
                self._check_for_defined_key(a_name, _path)
                self._key_regex(a_name, _path)
                self.required_keys.append(a_name)
        # Parse key restrictions
        self.key_restrictions = restrictions.pop("keys", {})
        a_path = f"{schema_path}.keys"
        nadap.schema.is_dict(self.key_restrictions, a_path)
        for a_name, a_restrictions in self.key_restrictions.items():
            a_n_path = f"{a_path}.{a_name}"
            self._check_for_defined_key(a_name, a_n_path)
            self._key_regex(a_name, a_n_path)
            self._parse_key_restrictions(
                restrictions=a_restrictions,
                schema_path=a_n_path,
            )
        # Parse xor_required:
        self.xor_required = restrictions.pop("xor_required", [])
        xor_path = f"{schema_path}.xor_required"
        nadap.schema.is_list(self.xor_required, xor_path)
        if self.xor_required and set(self.required_keys) == set(self.keys):
            raise SchemaDefinitionError(
                "Not allowed if all keys are required", xor_path
            )
        for index1, xor_list in enumerate(self.xor_required):
            xor_i_path = f"{xor_path}[{index1}]"
            nadap.schema.is_list(xor_list, xor_i_path)
            if len(xor_list) < 2:
                raise SchemaDefinitionError(
                    "List must have at least two key names", xor_i_path
                )
            for index2, a_name in enumerate(xor_list):
                _path = f"{xor_i_path}[{index2}]"
                self._check_for_defined_key(a_name, _path)
                self._key_regex(a_name, _path)
        nadap.schema.no_more_definition_options(
            definition=restrictions, source="restrictions", path=schema_path
        )

    def _convert_reference_data(self, data: any) -> any:
        if not self.reference_keys:
            return data
        ret_data = {}
        if self.regex_mode:
            for r_name in self.reference_keys:
                for a_name in data:
                    if self.regex_store[r_name].match(a_name):
                        ret_data[a_name] = data[a_name]
        else:
            for a_name in self.reference_keys:
                if a_name in data:
                    ret_data[a_name] = data[a_name]
        return ret_data

    def _pop_reference_definition(self, ref_definition: dict, schema_path: str):
        if "keys" in ref_definition:
            a_list = ref_definition.pop("keys")
            _path = f"{schema_path}.keys"
            nadap.schema.is_non_empty_list(a_list, _path)
            for index, a_name in enumerate(a_list):
                i_path = f"{_path}[{index}]"
                self._check_for_defined_key(a_name, i_path)
                self._key_regex(a_name, i_path)
            self.reference_keys = a_list

        super()._pop_reference_definition(
            ref_definition=ref_definition, schema_path=schema_path
        )

    def _validate_options(self, schema_path: str):
        super()._validate_options(schema_path=schema_path)
        self._validate_keys_option(
            schema_path=f"{schema_path}.keys",
        )
        self._validate_restrictions_option(schema_path=f"{schema_path}.restrictions")

    def _pop_options(self, definition: dict, schema_path: str):
        self.ignore_unknown_keys = definition.pop("ignore_unknown_keys", False)
        self.keys = definition.pop("keys", {})
        self.key_restrictions = definition.pop("restrictions", {})
        super()._pop_options(definition, schema_path)

    def _get_matching_regex_string(
        self, a_name: any, regex_strings: list[str]
    ) -> str | None:
        for re_str in regex_strings:
            re_obj = self.regex_store[re_str]
            if re_obj.match(a_name):
                return re_str
        return None

    def _test_a_name_in_data(self, a_name, data: dict) -> bool:
        if self.regex_mode:
            for data_key in data:
                if self.regex_store[a_name].match(data_key):
                    return True
        elif a_name in data:
            return True
        return False

    def _test_key_data(self, data, path, env):
        r_dict = {}
        for a_name in data:
            key_path = f"{path}.{a_name}"
            dt = None
            if self.regex_mode:
                def_key = self._get_matching_regex_string(a_name, list(self.keys))
                if def_key is not None:
                    dt = self.keys[def_key]
            elif a_name in self.keys:
                dt = self.keys[a_name]
            if dt:
                try:
                    a_data = dt.validate(
                        data=data[a_name],
                        path=key_path,
                        env=env,
                    )
                except DataValidationError:
                    r_dict = None
                else:
                    if r_dict is not None:
                        r_dict[a_name] = a_data
            elif not self.ignore_unknown_keys:
                env.findings.append(
                    nadap.results.ValidationFinding("Key not allowed", key_path)
                )
                r_dict = None
        if r_dict is None:
            raise DataValidationError()
        return r_dict

    def _test_required_keys(self, data, path, env):
        found_required = set()
        for a_name in self.required_keys:
            if self.regex_mode:
                for data_key in data:
                    if self.regex_store[a_name].match(data_key):
                        found_required.add(a_name)
                        break
            elif a_name in data:
                found_required.add(a_name)
        if missing_a_names := set(self.required_keys) - found_required:
            for a_name in missing_a_names:
                if self.regex_mode:
                    msg = f"No key found matching regex pattern '{a_name}'"
                else:
                    msg = f"Required key '{a_name}' not found"
                env.findings.append(nadap.results.ValidationFinding(msg, path))
            raise DataValidationError()

    def _test_required_xor(self, data, path, env):
        for a_list in self.xor_required:
            first_found = None
            for a_name in a_list:
                if self._test_a_name_in_data(a_name, data):
                    if first_found:
                        self._create_finding_with_error(
                            msg=f"Key {first_found} excludes key {a_name}",
                            path=path,
                            env=env,
                        )
                    first_found = "a_name"
            if not first_found:
                self._create_finding_with_error(
                    msg=f"One of these keys required: {', '.join(a_list)}",
                    path=path,
                    env=env,
                )

    def _test_key_restrictions(self, data, path, env):
        invalid = False
        for a_name in data:
            _path = f"{path}.{a_name}"
            a_restrictions = {}
            if self.regex_mode:
                if re_str := self._get_matching_regex_string(
                    a_name=a_name, regex_strings=list(self.key_restrictions)
                ):
                    a_restrictions = self.key_restrictions[re_str]
            else:
                a_restrictions = self.key_restrictions.get(a_name, {})
            if a_restrictions:
                for aa_name in a_restrictions.get("requires", []):
                    if not self._test_a_name_in_data(aa_name, data):
                        env.findings.append(
                            nadap.results.ValidationFinding(
                                f"Requires key '{aa_name}'", _path
                            )
                        )
                        invalid = True
                for aa_name in a_restrictions.get("excludes", []):
                    if self._test_a_name_in_data(aa_name, data):
                        env.findings.append(
                            nadap.results.ValidationFinding(
                                f"Excludes key '{aa_name}'", _path
                            )
                        )
                        invalid = True
        if invalid:
            raise DataValidationError()

    def _validate_data(
        self,
        data: any,
        path: str,
        env: "ValEnv" = None,
    ) -> "any":
        data = super()._validate_data(data=data, path=path, env=env)
        invalid = False
        # Check required keys:
        try:
            self._test_required_keys(data=data, path=path, env=env)
        except DataValidationError:
            invalid = True
        # Check required_xor keys:
        try:
            self._test_required_xor(data=data, path=path, env=env)
        except DataValidationError:
            invalid = True
        # Check key-specific restrictions
        try:
            self._test_key_restrictions(data=data, path=path, env=env)
        except DataValidationError:
            invalid = True
        # Validate keys in data
        try:
            attr_data = self._test_key_data(
                data=data,
                path=path,
                env=env,
            )
        except DataValidationError:
            invalid = True
        if invalid:
            raise DataValidationError()
        return attr_data

    def _set_default(self, data: any):
        """
        Set values of nested data types to default if missing.
        """
        if self.regex_mode or not self.keys:
            return data
        for a_name, dt in self.keys.items():
            if a_name not in data and dt.default_value is not UNDEFINED:
                data[a_name] = dt.default_value
        return data

    def _doc_key_restrictions(self, a_name: any) -> "str|list":
        if self.required_keys and a_name in self.required_keys:
            a_restrictions = ["required"]
        else:
            a_restrictions = []
        requires = set()
        excludes = set()
        for xor_list in self.xor_required:
            if a_name in xor_list:
                _list = xor_list[:]
                _list.remove(a_name)
                excludes.update(_list)
        if a_name in self.key_restrictions:
            requires.update(self.key_restrictions[a_name].get("requires", []))
            excludes.update(self.key_restrictions[a_name].get("excludes", []))
        if requires or excludes:
            if requires:
                if len(requires) == 1:
                    a_restrictions.append(f"requires: {requires.pop()}")
                else:
                    a_restrictions.append("requires:")
                    a_restrictions += [
                        f" - {str(number_to_str_number(x))}" for x in sorted(requires)
                    ]
            if excludes:
                if len(excludes) == 1:
                    a_restrictions.append(f"excludes: {excludes.pop()}")
                else:
                    a_restrictions.append("excludes:")
                    a_restrictions += [
                        f" - {str(number_to_str_number(x))}" for x in sorted(excludes)
                    ]
        return a_restrictions

    @property
    def markdown_table_rows(self) -> "list[nadap.schema.DocTableRow]":
        """
        Get markdown table rows for this data type definition
        """
        ret_list = super().markdown_table_rows
        if self.keys:
            for a_name in self.keys:
                a_list = self.keys[a_name].markdown_table_rows
                # Set variable for key row
                a_list[0].variable = a_name
                a_list[0].restrictions = (
                    self._doc_key_restrictions(a_name) + a_list[0].restrictions
                )
                for x in a_list[1:]:
                    x.indents.insert(0, self._markdown_indent)
                ret_list += a_list
        return ret_list

    @property
    def doc_yaml(self) -> "list[str]":
        """
        Get data structure
        """
        if not self.keys:
            return ["{}"]
        ret_list = []
        for a_name, a_dt in self.keys.items():
            a_list = a_dt.doc_yaml
            if dict in a_dt.python_classes or list in a_dt.python_classes:
                # key is not a leaf
                if len(a_list) == 1 and a_list[0] == "{}":
                    ret_list.append(f"{a_name}: {a_list[0]}")
                else:
                    ret_list.append(f"{a_name}:")
                    ret_list += [f"  {x}" for x in a_list]
            else:
                ret_list.append(f"{a_name}: {a_list[0]}")
        return ret_list

    @classmethod
    def _doc_options_md_upper_part(cls) -> list[str]:
        return super()._doc_options_md_upper_part() + [
            "| **keys** | <code>dict[dict&#124;str]</code> | | | |",
            "| &nbsp;&nbsp;< key_name > | <code>dict&#124;str</code> | | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;*option 1* | `str` | | "
            + "Data type str (short definition) |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;*option 2* | `dict` | | "
            + "Data type definition |",
            "| **restrictions** | `dict` | | | |",
            "| &nbsp;&nbsp;**required** | <code>list[str]&#124;str</code> | | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;*option 1* | `str` | | Allowed_value: all | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;*option 2* | `list[str]` | | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;- < key_name > | `str` | | | |",
            "| &nbsp;&nbsp;**keys** | `dict`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;**< key_name >** | `dict`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**excludes** | `list[str]`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**< key_name >** | `str`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**requires** | `list[str]`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**< key_name >** | `str`| | | |",
            "| &nbsp;&nbsp;**xor_required** | `list[list]`| | | |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;**-** | `list[str]`| | Min length: 2 | "
            + "Data's keys must match one and only one of these |",
            "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**- < key_name >** | `str`| | | |",
            "| **ignore_unknown_keys** | ``bool`` | false | | |",
        ]

    @classmethod
    def _doc_options_yaml_upper_part(cls) -> list[str]:
        return super()._doc_options_yaml_upper_part() + [
            "",
            "keys:",
            "  <key_name>:",
            "    # Multitype!!!",
            "    <str>",
            "    # or",
            "    <dict>",
            "restrictions:",
            "  required:",
            "    # Multitype!!!",
            "    'all'",
            "    # or",
            "    - <str>",
            "  keys:",
            "    excludes:",
            "      - <key_name>",
            "    requires:",
            "      - <key_name>",
            "  xor_required:",
            "    -",
            "      - <key_name>",
            "ignore_unknown_keys: <true|false",
        ]


DOC_DT_CLASS = Dict  # pylint: disable=invalid-name
