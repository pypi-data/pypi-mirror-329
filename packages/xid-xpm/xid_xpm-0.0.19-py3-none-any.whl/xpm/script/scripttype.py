#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from enum import Enum, auto



#--------------------------------------------------------------------------------
# 스크립트 종류.
#--------------------------------------------------------------------------------
class ScriptType(Enum):
	#--------------------------------------------------------------------------------
	# 멤버 요소 목록.
	#--------------------------------------------------------------------------------
	INVALID = auto()
	BATCH = auto()
	SHELL = auto()