import io
import os
import subprocess
import sys

import pytest


@pytest.mark.commands
@pytest.mark.parametrize(
    "command",
    ["word2vec", "word2phrase", "word2vec-compute-accuracy", "word2vec-doc2vec"],
)
def test_command_exists(command):
    try:
        proc = subprocess.run(
            [command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        assert proc.returncode == 0
    except OSError as e:
        assert "" == e
