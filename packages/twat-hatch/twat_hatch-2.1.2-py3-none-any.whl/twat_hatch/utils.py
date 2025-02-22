'Utility functions for twat-hatch.'
from __future__ import annotations
_A=None
import re,sys
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class PyVer:
	'Python version representation.\n\n    Handles various Python version formats:\n    - Tuple: (3, 10, 0)\n    - String: "3.10" or "3.10.0" or "3.10 Final"\n    - Ruff format: "py310"\n    - sys.version_info\n    - Command-line input: "3,10" or (3,10)\n\n    If no version is specified, defaults to Python 3.10.\n    ';major:int=3;minor:int=10;micro:int=0
	def __post_init__(A):
		'Validate version numbers.'
		if A.minor<0 or A.minor>99:B=f"Invalid minor version: {A.minor}";raise ValueError(B)
		if A.micro<0:B=f"Invalid micro version: {A.micro}";raise ValueError(B)
	def __str__(A):"Convert to string format (e.g. '3.10').";return f"{A.major}.{A.minor:02d}"
	def __repr__(A):'Full representation including micro version.';return f"PyVer(major={A.major}, minor={A.minor}, micro={A.micro})"
	def as_tuple(A):'Get version as a tuple (major, minor, micro).';return A.major,A.minor,A.micro
	@property
	def ruff_target(self):"Get Ruff target version (e.g. 'py310').";return f"py{self.major}{self.minor:02d}"
	@property
	def mypy_version(self):"Get MyPy version string (e.g. '3.10').";return str(self)
	@property
	def classifier_version(self):"Get version string for Python classifier (e.g. '3.10').";return str(self)
	@property
	def full_version(self):"Get full version string (e.g. '3.10.0').";A=self;return f"{A.major}.{A.minor:02d}.{A.micro}"
	@classmethod
	def parse(G,version=_A):
		'Parse a version from various formats into a PyVer instance.\n\n        Args:\n            version: Version in any supported format or None for defaults\n                    Supports:\n                    - None (defaults to 3.10)\n                    - Tuple[int, ...] like (3, 10) or (3, 10, 0)\n                    - sys.version_info style object\n                    - String like "3.10" or "3.10.0" or "3.10 Final"\n                    - Ruff style string like "py310"\n\n        Returns:\n            PyVer instance with Python 3.10 as default\n\n        Raises:\n            ValueError: If version string is invalid\n        ';J='major';B=version
		if B is _A:return G(major=3,minor=10)
		if isinstance(B,tuple)or hasattr(B,J):
			try:
				E=int(getattr(B,J,B[0]));A=int(getattr(B,'minor',B[1]if len(B)>1 else 0));H=int(getattr(B,'micro',B[2]if len(B)>2 else 0))
				if A<0 or A>99:C=f"Invalid minor version: {A}";raise ValueError(C)
				return G(major=E,minor=A,micro=H)
			except(IndexError,AttributeError,ValueError)as I:C=f"Invalid version tuple/object: {B}";raise ValueError(C)from I
		F=str(B).strip().lower()
		if F.startswith('py'):
			D=re.match('py(\\d)(\\d{2,})',F)
			if D:
				E=int(D.group(1));A=int(D.group(2))
				if A<0 or A>99:C=f"Invalid minor version: {A}";raise ValueError(C)
				return G(major=E,minor=A)
			C=f"Invalid Ruff version format: {F}";raise ValueError(C)
		F=F.split()[0];D=re.match('(\\d+)\\.(\\d+)',F)
		if D:
			E=int(D.group(1));A=int(D.group(2))
			if A<0 or A>99:C=f"Invalid minor version: {A}";raise ValueError(C)
			return G(major=E,minor=A)
		D=re.match('(\\d+)\\.(\\d+)\\.(\\d+)',F)
		if D:
			E=int(D.group(1));A=int(D.group(2));H=int(D.group(3))
			if A<0 or A>99:C=f"Invalid minor version: {A}";raise ValueError(C)
			return G(major=E,minor=A,micro=H)
		try:E=int(F);return G(major=E,minor=0)
		except ValueError as I:C=f"Invalid version string: {F}";raise ValueError(C)from I
	@classmethod
	def from_sys_version(A):'Create PyVer from current Python version.';return A.parse(sys.version_info)
	@classmethod
	def get_supported_versions(F,min_ver,max_ver=_A):
		'Get list of supported Python version classifiers.\n\n        Args:\n            min_ver: Minimum Python version\n            max_ver: Maximum Python version or None\n\n        Returns:\n            List of Python version classifiers\n        ';B=min_ver;A=max_ver;C=12;D=A.minor if A else C
		if A and A.major!=B.major:E=f"Maximum Python version {A} must have same major version as minimum {B}";raise ValueError(E)
		return[f"Programming Language :: Python :: {B.major}.{A:02d}"for A in range(B.minor,D+1)]
	def requires_python(C,max_ver=_A):
		'Get requires-python string.\n\n        Args:\n            max_ver: Maximum Python version or None\n\n        Returns:\n            requires-python string (e.g. ">=3.10" or ">=3.10,<3.12")\n        ';A=max_ver;B=f">={C}"
		if A:B+=f",<{A}"
		return B
	@classmethod
	def from_cli_input(C,version=_A):
		'Parse Python version from command-line input.\n\n        Args:\n            version: Version in CLI format:\n                    - None (defaults to 3.10)\n                    - Tuple[int, ...] like (3, 10)\n                    - String like "3,10"\n\n        Returns:\n            PyVer instance with Python 3.10 as default\n\n        Raises:\n            ValueError: If version string is invalid or if float is provided\n        ';A=version
		if A is _A:return C(major=3,minor=10)
		if isinstance(A,float):B='Python version must be specified as comma-separated integers. Use: "3,10" NOT "3.10"';raise ValueError(B)
		if isinstance(A,tuple):
			if len(A)!=2:B='Version tuple must have exactly 2 elements';raise ValueError(B)
			return C(major=A[0],minor=A[1])
		if isinstance(A,str):
			try:D,E=map(int,A.split(','));return C(major=D,minor=E)
			except ValueError:B='Version string must be comma-separated integers (e.g. "3,10")';raise ValueError(B)
		B=f"Unsupported version format: {A}";raise ValueError(B)