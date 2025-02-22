'Core functionality for Python package initialization.'
from __future__ import annotations
_U='No configuration provided'
_T='mkdocs'
_S='use_vcs'
_R='use_mkdocs'
_Q='dev_dependencies'
_P='author_email'
_O='author_name'
_N='package'
_M='plugin_dependencies'
_L='development_status'
_K='license'
_J='github_username'
_I='min_python'
_H='git'
_G='plugin_host'
_F='max_python'
_E='dependencies'
_D='import_name'
_C=False
_B=None
_A=True
import subprocess
from datetime import datetime
from importlib.resources import path
from pathlib import Path
from typing import Any,cast
import tomli
from jinja2 import Environment,FileSystemLoader,select_autoescape
from pydantic import BaseModel,Field
from rich.console import Console
from twat_hatch.utils import PyVer
console=Console()
class TemplateEngine:
	'Jinja2-based template engine for package generation.'
	def __init__(A,themes_dir):'Initialize template engine with themes directory.\n\n        Args:\n            themes_dir: Base directory containing theme templates\n        ';A.loader=FileSystemLoader(str(themes_dir));A.env=Environment(loader=A.loader,autoescape=select_autoescape(),trim_blocks=_A,lstrip_blocks=_A,keep_trailing_newline=_A);A.env.filters['split']=lambda value,delimiter:value.split(delimiter);A.env.filters['strftime']=lambda format:datetime.now().strftime(format)
	def render_template(A,template_path,context):"Render a template with given context.\n\n        Args:\n            template_path: Path to template file relative to themes directory\n            context: Template variables\n\n        Returns:\n            Rendered template content\n\n        Raises:\n            jinja2.TemplateNotFound: If template doesn't exist\n        ";B=A.env.get_template(template_path);return B.render(**context)
	def apply_theme(G,theme_name,target_dir,context):
		'Apply a theme to target directory.\n\n        Args:\n            theme_name: Name of theme to apply\n            target_dir: Directory to write rendered files to\n            context: Template variables\n        ';L='__package_name__';K='hidden.';H=context;D=theme_name;A=Path(cast(list[str],G.loader.searchpath)[0])/D
		if not A.exists():M=f"Theme '{D}' not found";raise FileNotFoundError(M)
		for I in A.rglob('*.j2'):
			E=I.relative_to(A);B=list(E.parts)
			for(J,C)in enumerate(B):
				if C.startswith(K):B[J]=C.replace(K,'.')
				elif L in C:B[J]=C.replace(L,H[_D])
			E=Path(*B);F=target_dir/E.with_suffix('');F.parent.mkdir(parents=_A,exist_ok=_A);N=G.render_template(f"{D}/{I.relative_to(A)}",H);F.write_text(N,encoding='utf-8');console.print(f"Created: [cyan]{F}[/]")
class PackageConfig(BaseModel):
	'Stores configuration values for package generation.';packages:list[str]=Field(description='List of packages to initialize');plugin_host:str|_B=Field(_B,description='Optional plugin host package name');output_dir:Path|_B=Field(_B,description='Where to create packages');author_name:str=Field(...,description='Name of the package author');author_email:str=Field(...,description='Email of the package author');github_username:str=Field(...,description='GitHub username');min_python:str=Field(...,description='Minimum Python version required');max_python:str|_B=Field(_B,description='Maximum Python version supported (optional)');license:str=Field(...,description='Package license');development_status:str=Field(...,description='Package development status');dependencies:list[str]=Field(default_factory=list,description='Regular package dependencies');plugin_dependencies:list[str]=Field(default_factory=list,description='Additional dependencies for plugins');dev_dependencies:list[str]=Field(default_factory=list,description='Development dependencies');ruff_config:dict[str,Any]=Field(default_factory=dict);mypy_config:dict[str,Any]=Field(default_factory=dict);use_mkdocs:bool=Field(default=_C,description='Whether to use MkDocs for documentation');use_semver:bool=Field(default=_C,description='Whether to use semantic versioning');use_vcs:bool=Field(default=_C,description='Whether to initialize version control')
	@property
	def python_version_info(self):
		'Get Python version information in various formats needed by tools.\n\n        Returns:\n            Dictionary containing:\n            - requires_python: Version specifier string for pyproject.toml\n            - classifiers: List of Python version classifiers\n            - ruff_target: Target version for ruff\n            - mypy_version: Version for mypy config\n        ';C=self;A=PyVer.parse(C.min_python)or PyVer(3,10);B=PyVer.parse(C.max_python)if C.max_python else _B
		if B and B.major!=A.major:D=f"Maximum Python version {B} must have same major version as minimum {A}";raise ValueError(D)
		return{'requires_python':A.requires_python(B),'classifiers':PyVer.get_supported_versions(A,B),'ruff_target':A.ruff_target,'mypy_version':A.mypy_version}
	@classmethod
	def from_toml(L,config_path):
		"Create configuration from TOML file.\n\n        Args:\n            config_path: Path to configuration file\n\n        Returns:\n            Initialized PackageConfig instance\n\n        Raises:\n            FileNotFoundError: If config file doesn't exist\n            ValidationError: If required fields are missing or invalid\n        ";K='output_dir';J='packages';C=Path(config_path)
		if not C.exists():M=f"Missing config file: {C}";raise FileNotFoundError(M)
		A=tomli.loads(C.read_text());D=A.get('project',{});E=A.get('author',{});B=A.get(_N,{});G=A.get(_E,{});N=A.get('development',{});H=A.get('tools',{});F=A.get('features',{});O=PyVer.parse(B.get(_I))or PyVer(3,10);I=PyVer.parse(B.get(_F))if B.get(_F)else _B;P={J:D.get(J,[]),_G:D.get(_G),K:D.get(K),_O:E.get('name'),_P:E.get('email'),_J:E.get(_J),_I:str(O),_F:str(I)if I else _B,_K:B.get(_K),_L:B.get(_L),_E:G.get(_E,[]),_M:G.get(_M,[]),_Q:N.get('additional_dependencies',[]),'ruff_config':H.get('ruff',{}),'mypy_config':H.get('mypy',{}),_R:F.get(_T,_C),'use_semver':F.get('semver',_C),_S:F.get('vcs',_C)};return L(**P)
class PackageInitializer:
	'Manages creation of Python package structures.'
	@staticmethod
	def _convert_name(name,to_import=_A):'Convert between package name formats.\n\n        Args:\n            name: Package name to convert\n            to_import: If True, converts to import name (using underscores)\n                      If False, converts to distribution name (using hyphens)\n\n        Returns:\n            Converted name string\n        ';return name.replace('-','_')if to_import else name.replace('_','-')
	def __init__(A,out_dir=_B,config_path=_B,base_dir=_B):
		'Initialize package generator with output directory and optional config.\n\n        Args:\n            out_dir: Base directory for generated packages\n            config_path: Path to TOML configuration file\n            base_dir: Base directory for resolving relative paths (defaults to cwd)\n        ';E=base_dir;D=config_path;B=out_dir;A.config=_B;A.base_dir=Path(E)if E else Path.cwd()
		if D:
			A.config=PackageConfig.from_toml(D)
			if A.config.output_dir:
				C=Path(A.config.output_dir)
				if not C.is_absolute():B=str(A.base_dir/C)
				else:B=str(C)
		A.out_dir=Path(B)if B else A.base_dir
		with path('twat_hatch.themes','')as F:A.template_engine=TemplateEngine(Path(F))
	def _init_git_repo(C,pkg_path):
		"Initialize Git repository in target directory with 'main' branch.\n\n        Args:\n            pkg_path: Directory to initialize repository in\n        ";A=pkg_path
		try:subprocess.run([_H,'init'],cwd=A,check=_A,capture_output=_A,text=_A,shell=_C);subprocess.run([_H,'branch','-M','main'],cwd=A,check=_A,capture_output=_A,text=_A,shell=_C);console.print(f"[green]Initialized Git repo: {A} (branch: main)[/]")
		except(subprocess.CalledProcessError,FileNotFoundError)as B:console.print(f"[yellow]Git init failed: {B}[/]")
	def _create_github_repo(C,pkg_path,name):
		'Create and link GitHub repository using gh CLI.\n\n        Args:\n            pkg_path: Package directory path.\n            name: Package name from pyproject.toml (distribution name)\n        ';A=pkg_path;D=C.config.github_username;B=f"{D}/{name}"
		try:subprocess.run(['gh','repo','create',B,'--public','--source',str(A),'--remote=origin','--push'],cwd=A,check=_A,capture_output=_A,text=_A,shell=_C);console.print(f"[green]Linked GitHub repo: {B}[/]")
		except subprocess.CalledProcessError as E:console.print(f"[yellow]GitHub repo creation failed: {E}[/]")
	def _create_version_file(B,pkg_path,import_name):'Create empty __version__.py file in package source directory.\n\n        Args:\n            pkg_path: Base package directory\n            import_name: Python import name for the package\n        ';A=pkg_path/'src'/import_name/'__version__.py';A.parent.mkdir(parents=_A,exist_ok=_A);A.touch();console.print(f"[green]Created version file: {A}[/]")
	def _get_context(A,name):
		'Get template context for package.\n\n        Args:\n            name: Package name\n\n        Returns:\n            Template context dictionary\n        '
		if not A.config:F='Configuration not loaded';raise RuntimeError(F)
		B=name.replace('-','_');C=B
		if A.config.plugin_host:
			D=f"{A.config.plugin_host}_"
			if B.startswith(D):C=B[len(D):]
			elif B.startswith(A.config.plugin_host):
				C=B[len(A.config.plugin_host):]
				if C.startswith(('-','_')):C=C[1:]
		E={'name':name,_D:B,'plugin_import_name':C,_O:A.config.author_name,_P:A.config.author_email,_J:A.config.github_username,_I:A.config.min_python,_F:A.config.max_python,_K:A.config.license,_L:A.config.development_status,_E:A.config.dependencies,_M:A.config.plugin_dependencies,_Q:A.config.dev_dependencies,_R:A.config.use_mkdocs,_S:A.config.use_vcs,'python_version_info':A.config.python_version_info}
		if A.config.plugin_host:E[_G]=A.config.plugin_host
		return E
	def initialize_package(A,name):
		'Initialize a package with appropriate theme.\n\n        Args:\n            name: Name of package to create (distribution name with hyphens)\n        ';D=name
		if not A.config:E=_U;raise ValueError(E)
		F=A._convert_name(D,to_import=_A);C=A._get_context(D);B=A.out_dir/F;G=B/'src'/C[_D];G.mkdir(parents=_A,exist_ok=_A);A.template_engine.apply_theme('default',B,C)
		if A.config.plugin_host:
			if D==A.config.plugin_host:A.template_engine.apply_theme(_G,B,C)
			else:A.template_engine.apply_theme('plugin',B,C)
		else:A.template_engine.apply_theme(_N,B,C)
		if A.config.use_mkdocs:A.template_engine.apply_theme(_T,B,C)
		A._create_version_file(B,C[_D])
		if A.config.use_vcs:
			A._init_git_repo(B)
			try:subprocess.run([_H,'add','.'],cwd=B,check=_A,capture_output=_A,text=_A,shell=_C);subprocess.run([_H,'commit','-m','Initial commit'],cwd=B,check=_A,capture_output=_A,text=_A,shell=_C);console.print(f"[green]Created initial commit in: {B}[/]")
			except(subprocess.CalledProcessError,FileNotFoundError)as H:console.print(f"[yellow]Git commit failed: {H}[/]")
			if A.config.github_username:A._create_github_repo(B,D)
	def initialize_all(A):
		'Initialize all packages specified in config.\n\n        The initialization order is:\n        1. Initialize plugin_host first (if specified AND included in packages)\n        2. Initialize all other packages\n        '
		if not A.config:C=_U;raise ValueError(C)
		if A.config.plugin_host and A.config.plugin_host in A.config.packages:A.initialize_package(A.config.plugin_host)
		for B in A.config.packages:
			if B!=A.config.plugin_host:A.initialize_package(B)