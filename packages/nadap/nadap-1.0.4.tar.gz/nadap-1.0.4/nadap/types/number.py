"""
Number data type classes
"""

# pylint: disable=too-few-public-methods

import nadap.schema
import nadap.types.base
import nadap.mixin.accuracy
import nadap.mixin.not_allowed_value
import nadap.mixin.min_max
import nadap.mixin.allowed_value

DOC_DT_NAME = "Number"
DOC_DT_DESCRIPTION = """
A **number** data type tests data for being an instance of
python's built-in class `float` or `int`.

> If using *number* data type with allowed values defined, check *enum* data type as a better option.
"""
DOC_DT_FEATURES = """
- Validate minimal and maximal data value
- Validate against allowed and not allowed number values
- Supports **Referencing Feature**
"""
DOC_DT_YAML_EXAMPLE = """
type: number
description: "Example number definition"

minimum: 1
maximum: 3.0

not_allowed_values:
  - 3.0
  - 1
  - 0.9

reference: ref_key
"""


class Number(
    nadap.mixin.accuracy.AccuracyMixin,
    nadap.mixin.not_allowed_value.NotAllowedValueMixin,
    nadap.mixin.allowed_value.AllowedValueMixin,
    nadap.mixin.min_max.MinMaxValueMixin,
    nadap.types.base.BaseType,
):
    """
    Number datatype class
    Includes integer and floats
    """

    data_type_name = "number"
    _cls_python_classes = [int, float]
    _convert_to_classes = {"str": str, "float": float, "int": int}
    _doc_data_type = "int|float"


DOC_DT_CLASS = Number  # pylint: disable=invalid-name
