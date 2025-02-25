#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from xpl import Console, BaseManager
from .semanticversiondata import SemanticVersionData


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"


#--------------------------------------------------------------------------------
# 버전 매니저.
#--------------------------------------------------------------------------------
class VersionManager(BaseManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__versionData: SemanticVersionData


	#--------------------------------------------------------------------------------
	# 버전 데이터 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def VersionData(thisInstance) -> SemanticVersionData:
		return thisInstance.__versionData
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__versionData = SemanticVersionData.CreateVersionDataFromVersionString("0.0.0")


	#--------------------------------------------------------------------------------
	# 버전 파일에서 버전 데이터 로드.
	#--------------------------------------------------------------------------------
	def Load(thisInstance, versionFilePath: str) -> bool:
		if not versionFilePath:
			return False
		if not os.path.isfile(versionFilePath):
			return False
		try:
			versionString: str = SemanticVersionData.CreateVersionStringFromVersionFile(versionFilePath)
			thisInstance.__versionData.SetVersionString(versionString)
			return True
		except Exception as exception:
			Console.Print(exception)
			return False


	#--------------------------------------------------------------------------------
	# 버전 데이터를 버전 파일로 저장.
	#--------------------------------------------------------------------------------
	def Save(thisInstance, versionFilePath: str) -> bool:
		if not versionFilePath:
			return False
		if not os.path.isfile(versionFilePath):
			return False
		try:
			versionString: str = thisInstance.__versionData.GetVersionString()
			SemanticVersionData.CreateVersionStringToVersionFile(versionFilePath, versionString)
			return True
		except Exception as exception:
			Console.Print(exception)
			return False