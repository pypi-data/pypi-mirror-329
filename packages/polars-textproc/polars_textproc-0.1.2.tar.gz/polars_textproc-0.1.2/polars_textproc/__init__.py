from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List

import polars as pl
from polars.plugins import register_plugin_function

from polars_textproc._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_textproc.typing import IntoExprColumn

LIB = Path(__file__).parent


def repetition_signals(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="repetition_signals",
        is_elementwise=True,
    )

def fasttext(expr: IntoExprColumn, *, path: str, labels: List[str], output_aggregate: bool = True, output_scores: bool = False) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="fasttext",
        is_elementwise=True,
        kwargs={'path': path, 'labels': labels, 'output_aggregate': output_aggregate, 'output_scores': output_scores},
    )
