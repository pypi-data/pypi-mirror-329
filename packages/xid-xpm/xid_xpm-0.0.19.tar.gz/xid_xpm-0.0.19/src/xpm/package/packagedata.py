#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from xpl import Console, BaseClass


#--------------------------------------------------------------------------------
# 패키지 데이터.
#--------------------------------------------------------------------------------
class PackageData(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__name: str
	__version: str
	__targetServer: str

	__versionOperator: str
	__minVersion: str
	__maxVersion: str


	#--------------------------------------------------------------------------------
	# 패키지 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		return thisInstance.__name


	#--------------------------------------------------------------------------------
	# 패키지 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Version(thisInstance) -> str:
		return thisInstance.__version


	#--------------------------------------------------------------------------------
	# 패키지 다운로드 주소 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def TargetServer(thisInstance) -> str:
		return thisInstance.__targetServer


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__name: str = str()
		thisInstance.__version: str = str()
		thisInstance.__targetServer: str = str()