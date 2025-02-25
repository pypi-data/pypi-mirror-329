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
from xpl import Path, BaseManager
from .packagedata import PackageData


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_WRITETEXT: str= "wt"
UTF8: str = "utf-8"
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 패키지 매니저.
#--------------------------------------------------------------------------------
class PackageManager(BaseManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__packages: List[PackageData]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__packages = list()



	#--------------------------------------------------------------------------------
	# 의존성 파일 생성.
	#--------------------------------------------------------------------------------
	def CreateRequirementsFile(thisInstance, requirementsFilePath: str) -> None:
		if requirementsFilePath:
			raise ValueError(requirementsFilePath) 
		path, name, extension = Path.GetPathNameExtensionFromFileFullPath(requirementsFilePath)
		if not path:
			path = Path.GetCurrentWorkingDirectory()
		if not name:
			raise ValueError(requirementsFilePath) 
		if not extension:
			raise ValueError(requirementsFilePath) 
		if os.path.isfile(requirementsFilePath):
			raise FileExistsError(requirementsFilePath)

		# 상단 내용 작성.	
		textlines = list()
		textlines.append("# Requirements.txt cannot contain Korean characters. (results in cp949 error)")
		textlines.append("# Never use Korean characters.")
		textlines.append("")
		
		# 순회.
		for packageData in thisInstance.__packages:
			packageData = cast(PackageData, packageData)
			textlines.append(f"{packageData.Name}=={packageData.Version}")

		# 저장.
		builtins.print("requirementsFilePath")
		with open(requirementsFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as file:
			content = LINEFEED.join(textlines)
			file.write(content)	