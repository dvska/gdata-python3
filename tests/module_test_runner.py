#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder@gmail.com (Jeff Scudder)'

import unittest


class ModuleTestRunner(object):
    def __init__(self, module_list=None, module_settings=None):
        """Constructor for a runner to run tests in the modules listed.

        Args:
          module_list: list (optional) The modules whose test cases will be run.
          module_settings: dict (optional) A dictionary of module level varables
              which should be set in the modules if they are present. An
              example is the username and password which is a module variable
              in most service_test modules.
        """
        self.modules = module_list or []
        self.settings = module_settings or {}

    def RunAllTests(self):
        """Executes all tests in this objects modules list.

        It also sets any module variables which match the settings keys to the
        corresponding values in the settings member.
        """
        runner = unittest.TextTestRunner(verbosity=2)
        for module in self.modules:
            # Set any module variables according to the contents in the settings
            for setting, value in self.settings.items():
                try:
                    setattr(module, setting, value)
                except AttributeError:
                    # This module did not have a variable for the current setting, so
                    # we skip it and try the next setting.
                    pass
            # We have set all of the applicable settings for the module, now
            # run the tests.
            result = runner.run(unittest.defaultTestLoader.loadTestsFromModule(module))
            if not result.wasSuccessful():
                raise Exception('Tests failed!')
