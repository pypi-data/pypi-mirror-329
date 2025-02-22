#!/usr/bin/env python3
'Configuration generation and management for twat-hatch.'
from __future__ import annotations
_D='plugin-host'
_C='package'
_B='plugin'
_A=True
from dataclasses import dataclass
from importlib.resources import path
from pathlib import Path
from typing import Any,Literal
from jinja2 import Environment,FileSystemLoader,select_autoescape
from twat_hatch.utils import PyVer
PackageType=Literal[_C,_B,_D]
@dataclass
class PackageTemplate:'Package template information.';type:PackageType;description:str;template_path:str
PACKAGE_TEMPLATES={_C:PackageTemplate(type=_C,description='Standalone Python package',template_path='package.toml.j2'),_B:PackageTemplate(type=_B,description='Plugin package for a plugin host',template_path='plugin.toml.j2'),_D:PackageTemplate(type=_D,description='Plugin host package that can load plugins',template_path='plugin_host.toml.j2')}
class ConfigurationGenerator:
	'Generates package configuration files.'
	def __init__(A):
		'Initialize generator with template engine.'
		with path('twat_hatch.themes','')as B:A.loader=FileSystemLoader(str(B),followlinks=_A);A.env=Environment(loader=A.loader,autoescape=select_autoescape(),trim_blocks=_A,lstrip_blocks=_A,keep_trailing_newline=_A,auto_reload=_A);A.env.filters['split']=lambda value,delimiter:value.split(delimiter)
	def generate_config(S,package_type,interactive=_A,**T):
		'Generate configuration content.\n\n        Args:\n            package_type: Type of package to create\n            interactive: Whether to prompt for missing values (unused, handled by CLI)\n            **kwargs: Configuration values to use\n\n        Returns:\n            Configuration content as string\n        ';F='min_python';G='plugin_dependencies';H='dev_dependencies';I='dependencies';J='use_vcs';K='use_mkdocs';L='development_status';M='license';N='author_email';O='author_name';P='plugin_host';Q='name';R=package_type;D='max_python';E='github_username';U=PACKAGE_TEMPLATES[R];A=T.copy()
		if not A.get(Q):A[Q]='my-package'
		if R==_B and not A.get(P):A[P]='my-plugin-host'
		if not A.get(O):A[O]='AUTHOR_NAME'
		if not A.get(N):A[N]='author@example.com'
		if not A.get(E):A[E]=E
		if not A.get(M):A[M]='MIT'
		if not A.get(L):A[L]='4 - Beta'
		A[K]=bool(A.get(K,False));A[J]=bool(A.get(J,_A))
		if I not in A:A[I]=[]
		if H not in A:A[H]=[]
		if G not in A:A[G]=[]
		B=PyVer.parse(A.get(F))or PyVer(3,10);C=PyVer.parse(A.get(D))if A.get(D)else None;A[F]=str(B);A[D]=str(C)if C else None;A['python_version_info']={'requires_python':B.requires_python(C),'classifiers':PyVer.get_supported_versions(B,C),'ruff_target':B.ruff_target,'mypy_version':B.mypy_version};V=S.env.get_template(U.template_path);return V.render(**A)
	def write_config(A,package_type,output_path,interactive=_A,**B):'Generate and write configuration file.\n\n        Args:\n            package_type: Type of package to generate config for\n            output_path: Where to write the configuration file\n            interactive: Whether to prompt for values (unused, handled by CLI)\n            **kwargs: Optional pre-defined values\n        ';C=A.generate_config(package_type,interactive,**B);D=Path(output_path);D.write_text(C)