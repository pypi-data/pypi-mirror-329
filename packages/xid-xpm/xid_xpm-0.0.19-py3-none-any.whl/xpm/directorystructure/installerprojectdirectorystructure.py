#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from .projectdirectorystructure import ProjectDirectoryStructure


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
SPACE: str = " "
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 인스톨러 프로젝트 디렉토리 구조 클래스.
#--------------------------------------------------------------------------------
class InstallerProjectDirectoryStructure(ProjectDirectoryStructure):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__sourceRootDirectory: str
	__sources: Dict[str, str]
	__destinationRootDirectory: str
	__destinations: Dict[str, str]


	#--------------------------------------------------------------------------------
	# 소스 루트 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def SourceRootDirectory(thisInstance) -> str:
		return thisInstance.__sourceRootDirectory
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 루트 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def DestinationRootDirectory(thisInstance) -> str:
		return thisInstance.__destinationRootDirectory


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, destinationRootDirectory: str) -> None:
		base = super()
		base.__init__()
		thisInstance.__sourceRootDirectory: str = os.path.join(thisInstance.BuildDirectory, "source")
		thisInstance.__destinationRootDirectory: str = destinationRootDirectory
		thisInstance.__sources: Dict[str, str] = dict()
		thisInstance.__destinations: Dict[str, str] = dict()


	#--------------------------------------------------------------------------------
	# 소스 디렉토리 설정.
	#--------------------------------------------------------------------------------
	def SetSource(thisInstance, key: str, value: str) -> None:
		thisInstance.__sources[key] = value


	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 설정.
	#--------------------------------------------------------------------------------
	def SetDestination(thisInstance, key: str, value: str) -> None:
		thisInstance.__destinations[key] = value


	#--------------------------------------------------------------------------------
	# 소스 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetSource(thisInstance, key: str, defualt: Optional[str] = None) -> Optional[str]:
		return thisInstance.__sources.get(key, defualt)
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetDestination(thisInstance, key: str, defualt: Optional[str] = None) -> Optional[str]:
		return thisInstance.__destinations.get(key, defualt)
	

	#--------------------------------------------------------------------------------
	# 소스 디렉토리의 키 보유 여부 반환.
	#--------------------------------------------------------------------------------
	def HasSource(thisInstance, key: str) -> bool:
		return key in thisInstance.__sources
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리의 키 보유 여부 반환.
	#--------------------------------------------------------------------------------
	def HasDestination(thisInstance, key: str) -> bool:
		return key in thisInstance.__destinations
	

	#--------------------------------------------------------------------------------
	# 소스 디렉토리 전체 비우기.
	#--------------------------------------------------------------------------------
	def ClearSource(thisInstance) -> None:
		thisInstance.__sources.clear()


	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 전체 비우기.
	#--------------------------------------------------------------------------------
	def ClearDestination(thisInstance) -> None:
		thisInstance.__destinations.clear()