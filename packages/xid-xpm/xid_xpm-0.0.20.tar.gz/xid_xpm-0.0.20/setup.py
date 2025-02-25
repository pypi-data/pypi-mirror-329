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
import setuptools


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
READ: str = "r"


#--------------------------------------------------------------------------------
# 참조 메타 데이터 목록.
#--------------------------------------------------------------------------------
NAME: str = "xid-xpm"
# VERSION: str = "0.0.2" # 접두어 v 붙여도 알아서 정규화하면서 제거됨.
AUTHOR: str = "xidware"
AUTHOR_EMAIL: str = "developer@xidware.com"
DESCRIPTION: str = "Xidware Python project Manager"
LONG_DESCRIPTION_CONTENT_TYPE: str = "text/markdown"
URL: str = "https://xidware.com"
PYTHON_REQUIRES: str = ">=3.9.7" # 실제로는 3.10.11 이상.
LONGDESCRIPTION: str = str()
with open(file = "README.md", mode = READ, encoding = UTF8) as file: LONGDESCRIPTION = file.read()
with open(file = "VERSION", mode = READ, encoding = UTF8) as file: VERSION = file.read()


#--------------------------------------------------------------------------------
# 빌드.
#--------------------------------------------------------------------------------
setuptools.setup(
	name = NAME,
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	description = DESCRIPTION,
	long_description = LONGDESCRIPTION,
	long_description_content_type = LONG_DESCRIPTION_CONTENT_TYPE,
	url = URL,
	packages = setuptools.find_packages(where = "src"),
	include_package_data = True,
	package_dir = { "": "src" },
	package_data = {
		"": [
			"res/*"
		],
	},
	scripts = [

	],
	entry_points = {
		"console_scripts": [
			"xpm=xpm.commandmanager:CommandManager.Run"
			# "venv=xpm.commandmanager:CommandManager.Run",
			# "service=xpm.commandmanager:CommandManager.Run"
		]
	},
	install_requires = [
		"xid-xpl"
	],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires = PYTHON_REQUIRES
)