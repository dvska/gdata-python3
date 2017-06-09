#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder@gmail.com (Jeff Scudder)'

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))
# print(sys.path)

from tests import run_data_tests
from tests import run_service_tests

if __name__ == '__main__':
    run_data_tests.RunAllTests()
    run_service_tests.GetValuesForTestSettingsAndRunAllTests()
