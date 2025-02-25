#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from enum import Enum, auto
from xpl import Console
from xpl import PlatformType, Environment


#--------------------------------------------------------------------------------
# 스크립트 기능 종류.
#--------------------------------------------------------------------------------
class ScriptFunctionType(Enum):
	#--------------------------------------------------------------------------------
	# 멤버 요소 목록.
	#--------------------------------------------------------------------------------
	NONE = auto() # required.

	# 가상 환경.
	VENV_CREATE = auto() # required.
	VENV_DESTROY = auto() # required.
	VENV_ENABLE = auto() # required.
	VENV_DISABLE = auto() # required.
	VENV_UPDATE = auto() # required.
	VENV_CREATE_FORCE = auto() # optional.
	VENV_UPDATE_FORCE = auto() # optional.

	# 실행.
	EXECUTE_SOURCE = auto() # required.
	EXECUTE_TEST = auto()

	# 빌드.
	BUILD_EXECUTABLE = auto() # required.
	BUILD_ARCHIVE = auto() # required.
	BUILD_MSI = auto()


	# 서비스.
	# Windows (service / nssm)
	# Linux (servicectl)
	# MacOS (brew / launchctl)
	SERVICE_REGISTER = auto()
	SERVICE_UNREGISTER = auto()
	SERVICE_START = auto()
	SERVICE_STOP = auto()
	SERVICE_RESTART = auto()
	SERVICE_STATUS = auto()
	SERVICE_UPDATE_DEPLOY = auto()

	# 로그.
	JOURNAL = auto()

	# 웹서버.
	NGINX_SERVICE_RELOAD = auto()
	NGINX_SERVICE_TEST = auto()