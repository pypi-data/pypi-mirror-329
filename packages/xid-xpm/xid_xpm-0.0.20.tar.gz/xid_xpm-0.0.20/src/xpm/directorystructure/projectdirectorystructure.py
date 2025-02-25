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
from xpl import Path


#--------------------------------------------------------------------------------
# 프로젝트 디렉토리 구조 클래스.
#--------------------------------------------------------------------------------
class ProjectDirectoryStructure():
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__rootDirectory: str
	__buildDirectory: str
	__resourceDirectory: str
	__sourceDirectory: str


	#--------------------------------------------------------------------------------
	# 루트 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def RootDirectory(thisInstance) -> str:
		return thisInstance.__rootDirectory


	#--------------------------------------------------------------------------------
	# 빌드 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def BuildDirectory(thisInstance) -> str:
		return thisInstance.__buildDirectory


	#--------------------------------------------------------------------------------
	# 리소스 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ReourceDirectory(thisInstance) -> str:
		return thisInstance.__resourceDirectory


	#--------------------------------------------------------------------------------
	# 소스 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def SourcePath(thisInstance) -> str:
		return thisInstance.__sourceDirectory


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		base = super()
		base.__init__()
		thisInstance.__rootDirectory: str = Path.GetRootPath(__file__)
		thisInstance.__sourceDirectory: str = os.path.join(thisInstance.__rootDirectory, "src")
		thisInstance.__resourceDirectory: str = os.path.join(thisInstance.__rootDirectory, "res")
		thisInstance.__buildDirectory: str = os.path.join(thisInstance.__rootDirectory, "build")
