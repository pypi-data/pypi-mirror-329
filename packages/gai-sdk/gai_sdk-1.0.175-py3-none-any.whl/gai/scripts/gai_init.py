from pathlib import Path
from rich.console import Console
import shutil
import json,os
import importlib.resources as pkg_resources

PACKAGED_DATA_PATH = pkg_resources.path('gai.scripts.data', '')
PACKAGED_CONFIG_PATH = pkg_resources.path('gai.scripts.data', 'gai.yml')

def init(force=False):
    console=Console()

    # Initialise config

    if not force and (Path("~/.gairc").expanduser().exists() or Path("~/.gai").expanduser().exists()):
        console.print("[red]Already exists[/]")
        return
    
    # app_dir doesn't exist
    if not Path("~/.gai").expanduser().exists():
        Path("~/.gai").expanduser().mkdir()

    # models directory doesn't exist
    if not Path("~/.gai/models").expanduser().exists():
        Path("~/.gai/models").expanduser().mkdir()

    # source_persona_path = PACKAGED_DATA_PATH / "persona"
    
    # if not Path("~/.gai/persona/nodes").expanduser().exists():
    #     Path("~/.gai/persona/nodes").expanduser().mkdir(parents=True)
        
    #     # cp -rp gai-data/src/gai/data/persona/* ~/.gai/persona/nodes
    #     for item in Path(source_persona_path).glob("*"):
    #         if item.is_dir():
    #             shutil.copytree(item, Path("~/.gai/persona/nodes").expanduser() / item.name)
    #         else:
    #             shutil.copy(item, Path("~/.gai/persona/nodes").expanduser() / item.name)

    # Force create .gairc
    with open(Path("~/.gairc").expanduser(), "w") as f:
        f.write(json.dumps({
            "app_dir":"~/.gai"
        }))

    # Finally
    if Path("~/.gairc").expanduser().exists() and Path("~/.gai").expanduser().exists():
        console.print("[green]Initialized[/]")
    
    # Copy all files in PACKAGED_DATA_PATH to ~/.gai
    DESTINATION = Path("~/.gai").expanduser()
    ignore_patterns = shutil.ignore_patterns('__pycache__', '__init__.py')    
    for item in PACKAGED_DATA_PATH.glob("*"):
        if item.is_dir():
            shutil.copytree(
                item,
                DESTINATION / item.name,
                ignore=ignore_patterns
            )
        else:
            # Skip __init__.py files in the top-level
            if item.name != '__init__.py':
                shutil.copy(item, DESTINATION / item.name)        
        
    
if __name__=="__main__":
    init(True)