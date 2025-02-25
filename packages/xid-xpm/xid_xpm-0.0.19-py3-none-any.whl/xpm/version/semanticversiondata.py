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
RE_CHECKVALIDATEVERSION: str = "^[0-9]+\\.[0-9]+\\.[0-9]+$"
DEFAULT_VERSIONSTRING: str = "0.0.0"
DOT: str = "."


#--------------------------------------------------------------------------------
# 시맨틱 버전 데이터.
# - Major.Minor.Patch의 3가지 단계적 정수로 구분하는 표준 표기법을 사용.
# - 상황에 따라 v를 붙이는 경우도 있으나 버전 데이터 자체에서는 v를 붙이지 않음.
#--------------------------------------------------------------------------------
class SemanticVersionData(VersionData):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__majorVersion: int
	__minorVersion: int
	__patchVersion: int


	#--------------------------------------------------------------------------------
	# 메이저 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def MajorVersion(thisInstance) -> int:
		return thisInstance.__majorVersion


	#--------------------------------------------------------------------------------
	# 메이저 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@MajorVersion.setter
	def MajorVersion(thisInstance, majorVersion: int) -> None:
		thisInstance.SetVersion(majorVersion, thisInstance.__minorVersion, thisInstance.__patchVersion)
	

	#--------------------------------------------------------------------------------
	# 마이너 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def MinorVersion(thisInstance) -> int:
		return thisInstance.__minorVersion


	#--------------------------------------------------------------------------------
	# 마이너 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@MinorVersion.setter
	def MinorVersion(thisInstance, minorVersion: int) -> None:
		thisInstance.SetVersion(thisInstance.__majorVersion, minorVersion, thisInstance.__patchVersion)

	
	#--------------------------------------------------------------------------------
	# 패치 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def PatchVersion(thisInstance) -> int:
		return thisInstance.__patchVersion


	#--------------------------------------------------------------------------------
	# 패치 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@PatchVersion.setter
	def PatchVersion(thisInstance, patchVersion: int) -> None:
		thisInstance.SetVersion(thisInstance.__majorVersion, thisInstance.__minorVersion, patchVersion)


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드. (오버라이드)
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__majorVersion: int = 0
		thisInstance.__minorVersion: int = 0
		thisInstance.__patchVersion: int = 0
		base = super()
		base.__init__()


	#--------------------------------------------------------------------------------
	# 버전 설정. (시맨틱 버전 데이터 기준)
	#--------------------------------------------------------------------------------
	def SetVersion(thisInstance, majorVersion: int, minorVersion: int, patchVersion: int) -> None:
		thisInstance.SetVersionString(f"{majorVersion}.{minorVersion}.{patchVersion}")


	#--------------------------------------------------------------------------------
	# 버전 문자열 설정. (오버라이드)
	#--------------------------------------------------------------------------------
	def SetVersionString(thisInstance, versionString: str) -> None:
		try:
			# 유효성 검사.
			if not thisInstance.__class__.CheckValidateVersionString(versionString):
				raise ValueError(versionString)

			# 시맨틱 버전 분해.
			versions = versionString.split(DOT)
			thisInstance.__majorVersion = int(versions[0])
			thisInstance.__minorVersion = int(versions[1])
			thisInstance.__patchVersion = int(versions[2])

			# 기본 버전 설정.
			base = super()
			base.SetVersionString(versionString)
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 버전 문자열의 구조적 유효성 검사. (오버라이드)
	# - "정수.정수.정수" 형태의 문자열 구조만 허용한다.
	#--------------------------------------------------------------------------------
	@classmethod
	def CheckValidateVersionString(thisClassType, versionString: str) -> bool:
		if not versionString:
			return False
		if not re.fullmatch(RE_CHECKVALIDATEVERSION, versionString):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 버전 문자열 기본값. (오버라이드)
	#--------------------------------------------------------------------------------
	@classmethod
	def GetDefaultVersionString(thisClassType) -> str:
		return DEFAULT_VERSIONSTRING