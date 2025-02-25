#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import argparse
from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from xpl import Console


#--------------------------------------------------------------------------------
# 커맨드 매니저.
#--------------------------------------------------------------------------------
class CommandManager:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	value: str


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.value = "VALUE!!"


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Run() -> None:
		# Console.Print(f"xpm")
		# argumentParser: ArgumentParser = ArgumentParser(description = "XPM Description.")
		# argumentParser.add_argument("name", type = str, help = "Project Name.")
		# argumentParser.add_argument("--path", type = str, default = ".", help = "Project Path. (Absolute)")
		# args = argumentParser.parse_Args()
		# builtins.print(f"args.name: {args.name}")
		# builtins.print(f"args.path: {args.path}")

		Console.Print(f"xpm")
		argumentParser = ArgumentParser()
		argumentParser.add_argument("vscode", type = str, help = "use IDE")
		
		argumentParser.parse_args()

		