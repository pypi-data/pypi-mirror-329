#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import re
from .versiondata import VersionData


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
RE_CHECKVALIDATEVERSION: str = "^[0-9]+$"
DEFAULT_VERSIONSTRING: str = "0"


#--------------------------------------------------------------------------------
# 인크리멘털 버전 데이터.
# - 단일 정수가 상황에 따라 1씩 증가.
# - 상황에 따라 v를 붙이는 경우도 있으나 버전 데이터 자체에서는 v를 붙이지 않음.
#--------------------------------------------------------------------------------
class IncrementalVersionData(VersionData):
	#--------------------------------------------------------------------------------
	# 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Version(thisInstance) -> int:
		versionString: str = thisInstance.GetVersionString()
		return int(versionString)
	

	#--------------------------------------------------------------------------------
	# 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@Version.setter
	def Version(thisInstance, version: int) -> None:
		thisInstance.SetIncrementalVersion(version)
	

	#--------------------------------------------------------------------------------
	# 버전 설정. (인크리멘털 버전 데이터 기준)
	#--------------------------------------------------------------------------------
	def SetIncrementalVersion(thisInstance, version: int) -> None:
		thisInstance.SetVersionString(f"{version}")


	# #--------------------------------------------------------------------------------
	# # 버전 문자열 설정. (오버라이드)
	# # - 자체적인 멤버 변수 등의 요소가 없으므로 부모 자체의 버전 문자열 함수를 사용해도 무방.
	# #--------------------------------------------------------------------------------
	# def SetVersionString(thisInstance, versionString: str) -> None:
	# 	try:
	# 		# 유효성 검사.
	# 		if not thisInstance.__class__.CheckValidateVersionString(versionString):
	# 			raise ValueError(versionString)

	# 		# 기본 버전 설정.
	# 		base = super()
	# 		base.SetVersionString(versionString)
	# 	except Exception as exception:
	# 		raise


	#--------------------------------------------------------------------------------
	# 버전 문자열의 구조적 유효성 검사. (오버라이드)
	# - "정수" 형태의 문자열 구조만 허용한다.
	#--------------------------------------------------------------------------------
	@classmethod
	def CheckValidateVersionString(thisClassType, versionString: str) -> bool:
		if not versionString:
			return False
		if not re.fullmatch(RE_CHECKVALIDATEVERSION, versionString):
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 버전 문자열 기본값.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetDefaultVersionString(thisClassType) -> str:
		return DEFAULT_VERSIONSTRING