from .io import *
from .wordvectors import *
from .wordclusters import *
from .scripts_interface import *

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
