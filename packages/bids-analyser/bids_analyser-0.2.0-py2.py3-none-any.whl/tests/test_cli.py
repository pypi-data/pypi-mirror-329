# Copyright (C) 2024 APH10 Limited
# SPDX-License-Identifier: Apache-2.0

"""
BIDS CLI tests
"""
import importlib
import logging
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from bids.cli import main


class TestCLI:
    """Tests the BIDS CLI"""

    TEST_PATH = Path(__file__).parent.resolve()
    SCRIPT_NAME = "bids-analyser"

    def test_usage(self):
        """Test that the usage returns 0"""

        # No parameters will error
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME])
        assert e.value.args[0] == 10
        # Test that the usage returns 0
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "--help"])
        assert e.value.args[0] == 0

    def test_version(self):
        """Test that the version returns 0"""
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "--version"])
        assert e.value.args[0] == 0

    def test_invalid_parameter(self):
        """Test that invalid parameters exit with expected error code.
        ArgParse calls sys.exit(2) for all errors"""

        self.tempdir = "/tmp"

        # invalid command
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "non-existant"])
        assert e.value.args[0] == 2

        # bad parameter
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "--bad-param"])
        assert e.value.args[0] == 2

        # bad parameter (but good directory)
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "--bad-param", self.tempdir])
        assert e.value.args[0] == 2

        # worse parameter
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, "--bad-param && cat hi", self.tempdir])
        assert e.value.args[0] == 2

        # bad parameter after directory
        with pytest.raises(SystemExit) as e:
            main([self.SCRIPT_NAME, self.tempdir, "--bad-param;cat hi"])
        assert e.value.args[0] == 2


