import asyncio
import builtins
import sys
from typing import Any

PY311 = sys.version_info[0:2] >= (3, 11)
PY310 = sys.version_info[0:2] >= (3, 10)

if PY311:
    asyncio.coroutine = getattr(asyncio, "coroutine", lambda f: f)  # type: ignore[attr-defined]

if not PY310:

    async def anext(it: Any, default: Any = None) -> Any:
        return await it.__anext__(default=default)
else:
    anext = builtins.anext  # type: ignore[assignment]
