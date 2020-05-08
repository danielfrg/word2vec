from .io import load, load_clusters  # noqa
from .scripts_interface import doc2vec, word2clusters, word2phrase, word2vec  # noqa
from .wordclusters import WordClusters  # noqa
from .wordvectors import WordVectors  # noqa


try:
    from ._generated_version import version as __version__
except ImportError:
    # Package is not installed, parse git tag at runtime
    try:
        import setuptools_scm

        # Code duplicated from setup.py to avoid a dependency on each other
        def parse_git(root, **kwargs):
            """
            Parse function for setuptools_scm
            """
            from setuptools_scm.git import parse

            kwargs[
                "describe_command"
            ] = "git describe --dirty --tags --long --match '*[0-9]*'"
            return parse(root, **kwargs)

        __version__ = setuptools_scm.get_version("./", parse=parse_git)
    except ImportError:
        __version__ = None
