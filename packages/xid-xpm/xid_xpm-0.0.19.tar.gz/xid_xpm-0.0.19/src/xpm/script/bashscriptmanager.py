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
from xpl import Console
from xpl import PlatformType, Environment
from .basescriptmanager import BaseScriptManager
# Environment.GetPlatformType()


#--------------------------------------------------------------------------------
# 배쉬 스크립트 매니저.
# - 리눅스, 맥 스크립팅.
#--------------------------------------------------------------------------------
class BashScriptManager(BaseScriptManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__textlines: list


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		base = super()
		base.__init__()

		thisInstance.__textlines: list = list()