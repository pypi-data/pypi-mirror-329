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
from xpl import Console, BaseManager, PlatformType, Environment
from .scripttype import ScriptType
from .scriptfunctiontype import ScriptFunctionType
# Environment.GetPlatformType()


#--------------------------------------------------------------------------------
# 스크립트 매니저.
# - os 별로 현재 프로젝트에 맞는 스크립트를 생성.
#--------------------------------------------------------------------------------
class BaseScriptManager(BaseManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__textlines: list


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__textlines: list = list()


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Clear(thisInstance) -> None:
		thisInstance.__textlines.clear()


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def AddFunction(thisInstance, type: ScriptFunctionType) -> None:
		thisInstance.__textlines.clear()