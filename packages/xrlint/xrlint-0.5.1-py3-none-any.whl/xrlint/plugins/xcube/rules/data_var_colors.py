#  Copyright © 2025 Brockmann Consult GmbH.
#  This software is distributed under the terms and conditions of the
#  MIT license (https://mit-license.org/).

from xrlint.node import VariableNode
from xrlint.plugins.xcube.plugin import plugin
from xrlint.plugins.xcube.util import is_spatial_var
from xrlint.rule import RuleContext, RuleOp


@plugin.define_rule(
    "data-var-colors",
    version="1.0.0",
    type="suggestion",
    description=(
        "Spatial data variables should encode xcube color mappings in their metadata."
    ),
    docs_url=(
        "https://xcube.readthedocs.io/en/latest/cubespec.html#encoding-of-colors"
    ),
)
class DataVarColors(RuleOp):
    def validate_variable(self, ctx: RuleContext, node: VariableNode):
        array = node.array
        if not node.in_data_vars() or not is_spatial_var(array):
            return
        attrs = array.attrs
        color_bar_name = attrs.get("color_bar_name")
        if not color_bar_name:
            ctx.report("Missing attribute 'color_bar_name'.")
        else:
            color_value_min = attrs.get("color_value_min")
            color_value_max = attrs.get("color_value_max")
            if color_value_min is None or color_value_max is None:
                ctx.report(
                    "Missing both or one of 'color_value_min' and 'color_value_max'."
                )

            color_norm = attrs.get("color_norm")
            if color_norm and color_norm not in ("lin", "log"):
                ctx.report(
                    "Invalid value of attribute 'color_norm', should be 'lin' or 'log'."
                )
