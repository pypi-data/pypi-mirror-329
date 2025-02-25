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
import sys
import unittest
from unittest import TestLoader, TextTestRunner
from xpl import Console, Path, BaseManager



#--------------------------------------------------------------------------------
# 테스트 매니저. (유닛테스트 기반)
#--------------------------------------------------------------------------------
class TestManager(BaseManager):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__testLoader: TestLoader
	__textTestRunner: TextTestRunner


	#--------------------------------------------------------------------------------
	# 테스트로더 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def TestLoader(thisInstance) -> TestLoader:
		return thisInstance.__testLoader


	#--------------------------------------------------------------------------------
	# 텍스트테스트러너 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def TextTestRunner(thisInstance) -> TextTestRunner:
		return thisInstance.__textTestRunner


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__testLoader: TestLoader = TestLoader()
		thisInstance.__textTestRunner: TextTestRunner = TextTestRunner()


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Run() -> None:
		executableFilePath: str = os.path.abspath(sys.modules["__main__"].__file__)
		rootPath: str = Path.GetRootPath(executableFilePath)
		sourcePath: str = os.path.join(rootPath, "src")
		# testPath: str = os.path.join(rootPath, "test")

		# 루트 경로 추가.
		# 루트의 자식인 src와 test를 메인 패키지로 추가하기 위한 설정.
		if rootPath not in sys.path:
			sys.path.append(rootPath)
			Console.Print(f"[TestManager] Add Project Root: {rootPath}")

		# 소스 경로 추가.
		# src 안의 서브패키지들을 메인 패키지 처럼 src. 접근 없이 곧바로 사용하기 위한 설정.
		if sourcePath not in sys.path:
			sys.path.append(sourcePath)
			Console.Print(f"[TestManager] Add Source Packages: {sourcePath}")


		# test 디렉토리 내의 test_ 로 시작하는 모든 스크립트 파일을 기준으로 테스트 스위트 생성.
		# 생성된 테스트 스위트를 실행.
		testManager: TestManager = TestManager()
		suite = testManager.TestLoader.discover(start_dir = "test", pattern = "test_*.py")
		testManager.TextTestRunner.run(suite)

