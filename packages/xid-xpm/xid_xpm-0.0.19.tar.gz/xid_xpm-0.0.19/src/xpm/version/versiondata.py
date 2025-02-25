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
from xpl import BaseClass


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
DEFAULT_VERSIONSTRING: str = ""


#--------------------------------------------------------------------------------
# 버전 데이터.
# 일반적인 버전 표기법.
# - Semantic Versioning: 사실상 표준으로 세단계의 계층적 버전을 숫자로 표기. (major.minor.patch)
# - Date Based Versioning: 날짜 기반의 버전을 숫자로 표기. (2024.12.22 등)
# - Incremental Versioning: 릴리즈 할 때마다 단순히 숫자를 하나씩 증가시키고 이를 표기. 버전의 식별성을 높이기 위해 앞에 v를 접두어로 사용하는 경우도 있음. (32, v125 등)
# - Alphanumeric Versioning: 문자가 포함된 상태 버전을 표기. 개발단계, 빌드브랜치 여부 표현. 문자가들어갈때는 하이픈을 사용. (1.0-alpha, 1.3-beta, 1.2-rc1 등)
# - Build Number Versioning: 패치 대신 CI/CD기반의 프로덕트 빌드 번호로 관리. 빌드버전만 가지고 구분이 쉽고 고유번호라는 장점. (1.0.buildnumber)
# - Epoch Versioning: 특정 기준 시점(에포크)을 설정하고 이후의 변경에 대한 버전 관리. 에포크는 변할일이 드물기 때문에 Incremental로 표현. 또한 에포크는 접미어로 콜론을 사용. (1:major.minor.patch)
# - Branch or Revision Based Versioning: 소스 저장소의 브랜치명 혹은 리비전 번호를 활용. 리비전을 사용할 경우 접두어로 r을 붙이는게 일반적. (1.0-dev 2.3-r1234 등)
# - Hybrid Versioning: 사실상 위의 것들을 혼합하여 자체적인 방식으로 사용하는 경우. 패턴이 제각각이므로 공용체계로서 구분 할 수가 없음. (1.0.20241222, 2.0.45-alpha 등)
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = "VersionData")
class VersionData(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__versionString: str


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		versionString = thisInstance.__class__.GetDefaultVersionString()
		thisInstance.__versionString: str = versionString


	#--------------------------------------------------------------------------------
	# 버전 초기화.
	#--------------------------------------------------------------------------------
	def ResetVersion(thisInstance) -> None:
		versionString = thisInstance.__class__.GetDefaultVersionString()
		thisInstance.SetVersionString(versionString)


	#--------------------------------------------------------------------------------
	# 버전 설정.
	#--------------------------------------------------------------------------------
	def SetVersionString(thisInstance, versionString: str) -> None:
		try:
			# 유효성 검사.
			if not thisInstance.__class__.CheckValidateVersionString(versionString):
				raise ValueError(versionString)
			thisInstance.__versionString = versionString
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 버전 반환.
	#--------------------------------------------------------------------------------
	def GetVersionString(thisInstance) -> str:
		return thisInstance.__versionString


	#--------------------------------------------------------------------------------
	# 버전 문자열 반환.
	#--------------------------------------------------------------------------------
	def __str__(thisInstance) -> str:
		return thisInstance.GetVersionString()
	

	#--------------------------------------------------------------------------------
	# 버전 문자열 구조의 유효성 검사.
	#--------------------------------------------------------------------------------
	@classmethod
	def CheckValidateVersionString(thisClassType: Type[T], versionString: str) -> bool:
		return True
	

	#--------------------------------------------------------------------------------
	# 버전 문자열 기본값.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetDefaultVersionString(thisClassType: Type[T]) -> str:
		return DEFAULT_VERSIONSTRING
	

	#--------------------------------------------------------------------------------
	# 버전 문자열로 버전 데이터 생성.
	#--------------------------------------------------------------------------------	
	@classmethod
	def CreateVersionDataFromVersionString(thisClassType: Type[T], versionString: str) -> T:
		versionData = thisClassType()
		versionData.SetVersionString(versionString)
		return versionData
	

	#--------------------------------------------------------------------------------
	# 버전 파일에서 버전 문자열 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateVersionStringFromVersionFile(versionFilePath: str) -> str:
		if not versionFilePath:
			raise ValueError(versionFilePath)
		if not os.path.isfile(versionFilePath):
			raise FileNotFoundError(versionFilePath)
		with builtins.open(versionFilePath, mode = FILE_READTEXT, encoding = UTF8) as file:
			versionString: str = file.read()
			return versionString


	#--------------------------------------------------------------------------------
	# 버전 파일에서 버전 데이터 생성.
	#--------------------------------------------------------------------------------
	@classmethod
	def CreateVersionStringFromVersionFile(thisClassType: Type[T], versionFilePath: str) -> T:
		try:
			versionString: str = thisClassType.CreateVersionStringFromVersionFile(versionFilePath)
			versionData: T = thisClassType.CreateVersionDataFromVersionString(versionString)
			return versionData
		except Exception as exception:
			raise


	#--------------------------------------------------------------------------------
	# 버전 문자열로 버전 파일 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateVersionStringToVersionFile(versionFilePath: str, versionString: str) -> None:
		if not versionFilePath:
			raise ValueError(versionFilePath)
		if not os.path.isfile(versionFilePath):
			raise FileNotFoundError(versionFilePath)
		with builtins.open(versionFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as file:
			file.write(versionString)