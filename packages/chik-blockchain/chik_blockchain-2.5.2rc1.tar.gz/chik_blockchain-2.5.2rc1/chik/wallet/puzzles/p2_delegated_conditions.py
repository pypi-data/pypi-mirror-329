"""
Pay to delegated conditions

In this puzzle program, the solution must be a signed list of conditions, which
is returned literally.
"""

from __future__ import annotations

from chik.types.blockchain_format.program import Program
from chik.wallet.puzzles.load_klvm import load_klvm_maybe_recompile

MOD = load_klvm_maybe_recompile("p2_delegated_conditions.clsp")


def puzzle_for_pk(public_key: Program) -> Program:
    return MOD.curry(public_key)


def solution_for_conditions(conditions: Program) -> Program:
    return conditions.to([conditions])
