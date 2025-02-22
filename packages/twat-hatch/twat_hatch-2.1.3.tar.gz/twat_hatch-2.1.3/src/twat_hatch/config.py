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
		'Generate configuration content.\n\n        Args:\n            package_type: Type of package to create\n            interactive: Whether to prompt for missing values (unused, handled by CLI)\n            **kwargs: Configuration values to use\n\n        Returns:\n            Configuration content as string\n        ';R='min_python';Q='plugin_dependencies';P='dev_dependencies';O='dependencies';N='use_vcs';M='use_mkdocs';L='development_status';K='license';J='author_email';I='author_name';H='plugin_host';G='name';F=package_type;E='max_python';D='github_username';U=PACKAGE_TEMPLATES[F];A=T.copy()
		if not A.get(G):A[G]='my-package'
		if F==_B and not A.get(H):A[H]='my-plugin-host'
		if not A.get(I):A[I]='AUTHOR_NAME'
		if not A.get(J):A[J]='author@example.com'
		if not A.get(D):A[D]=D
		if not A.get(K):A[K]='MIT'
		if not A.get(L):A[L]='4 - Beta'
		A[M]=bool(A.get(M,False));A[N]=bool(A.get(N,_A))
		if O not in A:A[O]=[]
		if P not in A:A[P]=[]
		if Q not in A:A[Q]=[]
		B=PyVer.parse(A.get(R))or PyVer(3,10);C=PyVer.parse(A.get(E))if A.get(E)else None;A[R]=str(B);A[E]=str(C)if C else None;A['python_version_info']={'requires_python':B.requires_python(C),'classifiers':PyVer.get_supported_versions(B,C),'ruff_target':B.ruff_target,'mypy_version':B.mypy_version};V=S.env.get_template(U.template_path);return V.render(**A)
	def write_config(A,package_type,output_path,interactive=_A,**B):'Generate and write configuration file.\n\n        Args:\n            package_type: Type of package to generate config for\n            output_path: Where to write the configuration file\n            interactive: Whether to prompt for values (unused, handled by CLI)\n            **kwargs: Optional pre-defined values\n        ';C=A.generate_config(package_type,interactive,**B);D=Path(output_path);D.write_text(C)