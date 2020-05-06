from .io import *
from .wordvectors import *
from .wordclusters import *
from .scripts_interface import *

try:
    from ._generated_version import version as __version__
except ImportError:
    # Package is not installed, parse git tag at runtime
    try:
        import setuptools_scm
        def parse_git(root, **kwargs):
            """
            Parse function for setuptools_scm
            """
            from setuptools_scm.git import parse
            kwargs['describe_command'] = "git describe --dirty --tags --long"
            return parse(root, **kwargs)
        __version__ = setuptools_scm.get_version('./', parse=parse_git)
    except ImportError:
        __version__ = None
