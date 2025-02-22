#  Copyright © 2025 Brockmann Consult GmbH.
#  This software is distributed under the terms and conditions of the
#  MIT license (https://mit-license.org/).

import numpy as np

from xrlint.node import VariableNode
from xrlint.plugins.xcube.plugin import plugin
from xrlint.rule import RuleContext, RuleExit, RuleOp
from xrlint.util.formatting import format_count, format_seq


@plugin.define_rule(
    "increasing-time",
    version="1.0.0",
    type="problem",
    description="Time coordinate labels should be monotonically increasing.",
    docs_url=(
        "https://xcube.readthedocs.io/en/latest/cubespec.html#temporal-reference"
    ),
)
class IncreasingTime(RuleOp):
    def validate_variable(self, ctx: RuleContext, node: VariableNode):
        array = node.array
        if node.in_coords() and node.name == "time" and array.dims == ("time",):
            diff_array: np.ndarray = array.diff("time").values
            if not np.count_nonzero(diff_array > 0) == diff_array.size:
                check_indexes(ctx, diff_array == 0, "Duplicate")
                check_indexes(ctx, diff_array < 0, "Backsliding")
                raise RuleExit  # No need to apply rule any further


def check_indexes(ctx, cond: np.ndarray, issue_name: str):
    (indexes,) = np.nonzero(cond)
    if indexes.size > 0:
        index_text = format_count(indexes.size, singular="index", plural="indexes")
        ctx.report(
            f"{issue_name} 'time' coordinate label at {index_text}"
            f" {format_seq(indexes)}."
        )
