#!/usr/bin/env -S uv run
'Command-line interface for twat-hatch.\n\nThis module provides the main CLI interface for creating Python packages\nand plugins using twat-hatch.\n'
from __future__ import annotations
_P='twat-hatch.toml'
_O='package'
_N='my-plugin-host'
_M='plugin'
_L='use_vcs'
_K='use_mkdocs'
_J='development_status'
_I='license'
_H='max_python'
_G='min_python'
_F='github_username'
_E='author_email'
_D='author_name'
_C=False
_B=True
_A=None
import sys
from pathlib import Path
from typing import Any
import fire
from pydantic import ValidationError
from rich.ansi import AnsiDecoder
from rich.console import Console,Group
from rich.panel import Panel
from rich.prompt import Confirm,IntPrompt,Prompt
from rich.theme import Theme
from rich.traceback import install
from twat_hatch.config import ConfigurationGenerator,PackageType
from twat_hatch.hatch import PackageInitializer
from twat_hatch.utils import PyVer
install(show_locals=_B)
ansi_decoder=AnsiDecoder()
console=Console(theme=Theme({'prompt':'cyan','question':'bold cyan'}))
class ConfigurationPrompts:
	'Interactive configuration prompts.'
	def get_package_name(self,package_type):
		'Get package name from user.\n\n        Args:\n            package_type: Type of package being created\n\n        Returns:\n            Package name\n        ';default='my-package'
		if package_type==_M:default='my-plugin'
		elif package_type=='plugin-host':default=_N
		return Prompt.ask('[question]Package name[/]',default=default,show_default=_B)
	def get_plugin_host(self):'Get plugin host package name for plugins.\n\n        Returns:\n            Plugin host package name\n        ';return Prompt.ask('[question]Plugin host package name[/]',default=_N,show_default=_B)
	def get_author_info(self):'Get author information.\n\n        Returns:\n            Dictionary with author name, email, and GitHub username\n        ';return{_D:Prompt.ask('[question]Author name[/]',default='Your Name',show_default=_B),_E:Prompt.ask('[question]Author email[/]',default='your.email@example.com',show_default=_B),_F:Prompt.ask('[question]GitHub username[/]',default='yourusername',show_default=_B)}
	def get_python_versions(self):
		'Get Python version requirements.\n\n        Returns:\n            Dictionary with min_python and optional max_python\n        ';min_major=IntPrompt.ask('[question]Minimum Python major version[/]',default=3,show_default=_B);min_minor=IntPrompt.ask('[question]Minimum Python minor version[/]',default=10,show_default=_B);min_ver=PyVer(min_major,min_minor)
		if Confirm.ask('[question]Specify maximum Python version?[/]',default=_C,show_default=_B):max_major=IntPrompt.ask('[question]Maximum Python major version[/]',default=min_major,show_default=_B);max_minor=IntPrompt.ask('[question]Maximum Python minor version[/]',default=12,show_default=_B);max_ver=PyVer(max_major,max_minor);max_python=str(max_ver)
		else:max_python=_A
		return{_G:str(min_ver),_H:max_python}
	def get_package_info(self):'Get package information.\n\n        Returns:\n            Dictionary with license and development status\n        ';A='4 - Beta';return{_I:Prompt.ask('[question]License[/]',default='MIT',show_default=_B),_J:Prompt.ask('[question]Development status[/]',default=A,show_default=_B,choices=['1 - Planning','2 - Pre-Alpha','3 - Alpha',A,'5 - Production/Stable','6 - Mature','7 - Inactive'])}
	def get_features(self):'Get feature flags.\n\n        Returns:\n            Dictionary with feature flags\n        ';return{_K:Confirm.ask('[question]Use MkDocs for documentation?[/]',default=_C,show_default=_B),_L:Confirm.ask('[question]Initialize Git repository?[/]',default=_B,show_default=_B)}
def init(type=_O,output=_P,name=_A,author_name=_A,author_email=_A,github_username=_A,min_python=_A,max_python=_A,license=_A,development_status=_A,use_mkdocs=_A,use_vcs=_A,plugin_host=_A):
	'Initialize a new Python package or plugin.\n\n    Args:\n        type: Type of package to create ("package", "plugin", or "plugin-host")\n        output: Output path for configuration file\n        name: Package name\n        author_name: Author\'s name\n        author_email: Author\'s email\n        github_username: GitHub username\n        min_python: Minimum Python version as tuple (3,10) or string "3,10"\n        max_python: Maximum Python version as tuple (3,12) or string "3,12"\n        license: Package license\n        development_status: Package development status\n        use_mkdocs: Whether to use MkDocs for documentation\n        use_vcs: Whether to use version control\n        plugin_host: Host package name (for plugins only)\n\n    Note:\n        For Python versions, use comma-separated integers like "3,10" or (3,10).\n        Do NOT use decimal notation like "3.10" as it will be incorrectly parsed.\n    '
	try:
		try:min_ver=PyVer.from_cli_input(min_python);max_ver=PyVer.from_cli_input(max_python)if max_python is not _A else _A
		except ValueError as e:console.print(f"[red]Error: {e}[/]");sys.exit(1)
		user_provided_values={k:v for(k,v)in locals().items()if k in['name',_D,_E,_F,_G,_H,_I,_J,_K,_L,'plugin_host']and v is not _A};interactive=not bool(user_provided_values)
		if interactive:
			prompts=ConfigurationPrompts();name=prompts.get_package_name(type)
			if type==_M:plugin_host=prompts.get_plugin_host()
			author_info=prompts.get_author_info();author_name=author_info[_D];author_email=author_info[_E];github_username=author_info[_F];python_versions=prompts.get_python_versions();min_ver=PyVer.parse(python_versions[_G]);max_ver=PyVer.parse(python_versions.get(_H));package_info=prompts.get_package_info();license=package_info[_I];development_status=package_info[_J];features=prompts.get_features();use_mkdocs=features[_K];use_vcs=features[_L]
		config_generator=ConfigurationGenerator();config=config_generator.generate_config(package_type=type,interactive=_C,name=name,author_name=author_name,author_email=author_email,github_username=github_username,min_python=str(min_ver),max_python=str(max_ver)if max_ver else _A,license=license,development_status=development_status,use_mkdocs=use_mkdocs,use_vcs=use_vcs,plugin_host=plugin_host);output_path=Path(output);output_path.write_text(config);console.print(Panel(f"[green]Configuration written to {output_path}[/]\n[yellow]Run `twat-hatch create` to create the package[/]"))
	except ValidationError as e:console.print('[red]Error: Invalid configuration[/]');console.print(e);sys.exit(1)
	except Exception as e:console.print(f"[red]Error: {e}[/]");sys.exit(1)
def config(command='show',type=_O):
	'Show example configuration for a package type.\n\n    Args:\n        command: Command to execute (show)\n        type: Type of package to show config for\n    '
	if command!='show':console.print("[red]Invalid command. Use 'show'.[/]");sys.exit(1)
	try:generator=ConfigurationGenerator();content=generator.generate_config(type,interactive=_C);console.print(Panel(content,title=f"Example {type} configuration"))
	except Exception as e:console.print(f"[red]Error showing configuration: {e!s}[/]");sys.exit(1)
def create(config_path=_A):
	'Create packages from configuration.\n\n    Args:\n        config_path: Path to configuration file (defaults to twat-hatch.toml)\n    '
	if not config_path:config_path=_P
	try:initializer=PackageInitializer(config_path=config_path);initializer.initialize_all()
	except Exception as e:console.print(f"[red]Error creating packages: {e!s}[/]");sys.exit(1)
def main():
	'Main entry point.'
	def display(lines,out):console.print(Group(*map(ansi_decoder.decode_line,lines)))
	fire.core.Display=display;fire.Fire({'init':init,'config':config,'create':create})
if __name__=='__main__':main()