"""Vendored collective-choice organ (department D3), from `Mars_Governance` (family
`aigov-collective-choice`).

**Path shim, and why it is here rather than in the vendored code.** The organ's modules import each other
as top-level packages (`from governance.panel_agnostic import ...`), which is correct when its own
`conftest.py` puts this directory on `sys.path` — that is how its 193-test suite runs, unmodified, at full
strength. Rewriting those imports to relative form is the C2 namespace migration that family decision
**DV3 deliberately DEFERRED**: editing imports during a move risks a silent behaviour change in code whose
whole value is that it is known-good.

So instead of touching the vendored tree, this one line makes the same `sys.path` entry the vendored
conftest makes, at package-import time. The subtree stays byte-identical to its source; `aigov.kernel` can
import `aigov.choice.governance.*`; and the zero-test-loss bar keeps meaning what it says.

Known debt, recorded not hidden: two import styles now coexist for the same modules
(`governance.x` inside the subtree, `aigov.choice.governance.x` outside it). They resolve to the SAME
module object only because the shim runs first. Retiring this is the C2 migration.
"""

import os
import sys

_HERE = os.path.dirname(__file__)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
