import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

from puddlestuff import pluginloader
from puddlestuff.constants import MODULES

PLUGIN_NAME = 'puddletag_loader_test_plugin'


def _create_plugin(root, name):
    plugin_dir = os.path.join(root, name)
    os.makedirs(plugin_dir)
    with open(os.path.join(plugin_dir, 'info'), 'w', encoding='utf-8') as f:
        f.write(
            '[info]\n'
            'name = Loader Test Plugin\n'
            'author = puddletag tests\n'
            'version = 1.0\n'
            'puddletag_version = 2.5.0\n'
            'description = Plugin used by the plugin loader tests.\n'
        )
    with open(os.path.join(plugin_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('marker = True\n')
    return plugin_dir


class TestPluginLoader(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.addCleanup(sys.modules.pop, PLUGIN_NAME, None)

    def test_get_plugins_reads_plugin_info(self):
        _create_plugin(self.root, PLUGIN_NAME)

        plugins = pluginloader.get_plugins(self.root)

        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0][pluginloader.NAME], 'Loader Test Plugin')
        self.assertEqual(plugins[0][pluginloader.MODULE_NAME], PLUGIN_NAME)

    def test_user_plugin_outside_package_is_loaded(self):
        _create_plugin(self.root, PLUGIN_NAME)
        plugins = pluginloader.get_plugins(self.root)

        config = mock.Mock()
        config.get.return_value = [PLUGIN_NAME]
        plugin_dirs = [self.root,
                       os.path.join(os.path.dirname(pluginloader.__file__),
                                    'plugins')]
        with mock.patch.object(pluginloader, 'PuddleConfig',
                               return_value=config), \
                mock.patch.object(pluginloader, 'PLUGIN_DIRS', plugin_dirs):
            loaded = pluginloader.load_plugins(plugins=plugins)

        modules = loaded[MODULES]
        self.assertEqual(len(modules), 1)
        self.assertTrue(modules[0].marker)

    def test_bundled_plugins_still_load_as_package_submodules(self):
        module = pluginloader._import_plugin('view_all_fields')

        self.assertEqual(module.__name__,
                         'puddlestuff.plugins.view_all_fields')


if __name__ == "__main__":
    unittest.main()
