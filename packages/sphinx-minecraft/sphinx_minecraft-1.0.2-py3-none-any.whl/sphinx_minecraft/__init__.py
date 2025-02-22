from enum import Enum
import importlib
import os
from pathlib import Path
from sphinx.util import logging
from sphinx.application import Sphinx
from sphinx_treeview.decorator import DecoratorType, imagesToDecoratorIcons

logger = logging.getLogger(__name__)

__version__ = importlib.metadata.version('sphinx-minecraft')

class DectoratorRegistry(Enum):
    MCDIR = "mcdir"
    NBT = "nbt"
    
def add_static_path(app):
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "_static"))
    app.config.html_static_path.append(static_path)
    

def setup(app: Sphinx):
    app.setup_extension('sphinx_treeview')
    
    decorators = []
    
    for decorator in DectoratorRegistry:
        decorator_type = DecoratorType(decorator.value, imagesToDecoratorIcons(Path(__file__).parent / '_static' / 'smc' / 'images' / 'treeview_icons' / decorator.value, f"smc/images/treeview_icons/{decorator.value}"))
        decorators.append(decorator_type)
        logger.verbose(f"Tree decorator '{decorator.value}' added.")
    
    app.config.stv_decorators.extend(decorators)
    app.connect("builder-inited", add_static_path)
    
    return {
        "version": __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
    
    
    
