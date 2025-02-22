#  Copyright © 2025 Brockmann Consult GmbH.
#  This software is distributed under the terms and conditions of the
#  MIT license (https://mit-license.org/).

from xrlint.node import VariableNode
from xrlint.plugins.xcube.constants import LAT_NAME, LON_NAME, TIME_NAME, X_NAME, Y_NAME
from xrlint.plugins.xcube.plugin import plugin
from xrlint.rule import RuleContext, RuleOp


@plugin.define_rule(
    "cube-dims-order",
    version="1.0.0",
    type="problem",
    description=(
        f"Order of dimensions in spatio-temporal datacube variables"
        f" should be [{TIME_NAME}, ..., {Y_NAME}, {X_NAME}]."
    ),
    docs_url=(
        "https://xcube.readthedocs.io/en/latest/cubespec.html#data-model-and-format"
    ),
)
class CubeDimsOrder(RuleOp):
    def validate_variable(self, ctx: RuleContext, node: VariableNode):
        if node.in_data_vars():
            dims = list(node.array.dims)
            indexes = {d: i for i, d in enumerate(node.array.dims)}

            yx_names = None
            if X_NAME in indexes and Y_NAME in indexes:
                yx_names = [Y_NAME, X_NAME]
            elif LON_NAME in indexes and LAT_NAME in indexes:
                yx_names = [LAT_NAME, LON_NAME]
            else:
                # Note, we could get yx_names also from grid-mapping,
                # which would be more generic.
                pass
            if yx_names is None:
                # This rule only applies to spatial dimensions
                return

            t_name = None
            if TIME_NAME in indexes:
                t_name = TIME_NAME

            n = len(dims)
            t_index = indexes[t_name] if t_name else None
            y_index = indexes[yx_names[0]]
            x_index = indexes[yx_names[1]]

            yx_ok = y_index == n - 2 and x_index == n - 1
            t_ok = t_index is None or t_index == 0
            if not yx_ok or not t_ok:
                if t_index is None:
                    expected_dims = [d for d in dims if d not in yx_names] + yx_names
                else:
                    expected_dims = (
                        [t_name]
                        + [d for d in dims if d != t_name and d not in yx_names]
                        + yx_names
                    )
                # noinspection PyTypeChecker
                ctx.report(
                    f"Order of dimensions should be"
                    f" {','.join(expected_dims)}, but found {','.join(dims)}.",
                    suggestions=["Use xarray.transpose(...) to reorder dimensions."],
                )
