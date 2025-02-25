import os
import shutil
import unittest
from operator import itemgetter
from pathlib import Path
from tempfile import NamedTemporaryFile as NTFile, mkdtemp
from unittest import mock

import byuhbll_configuro as configuro
from byuhbll_configuro.core import INHERITANCE_SENTINEL


class LoadTests(unittest.TestCase):
    def test_all_args(self):
        with NTFile('w') as base_yml, NTFile('w') as config_yml:
            base_yml.write('debug: false\nverbose: false\na: 1\nb: 2')
            base_yml.flush()
            config_yml.write(
                f'extends: {base_yml.name}\ndebug: true\nverbose: true\nb: 5'
            )
            config_yml.flush()

            config = configuro.load(config_filename=config_yml.name)
            self.assertTrue(config.get('debug'))
            self.assertTrue(config.get('verbose'))
            self.assertTrue(config.get('a'), 1)
            self.assertTrue(config.get('b'), 5)

    def test_more_files_with_relative_paths(self):
        tmp_dir = mkdtemp()
        others_dir = os.path.join(tmp_dir, 'others')
        os.mkdir(others_dir)

        with open(os.path.join(tmp_dir, 'config.base.yml'), 'w') as base:
            base.write('debug: false\nverbose: false\na: 1\nb: 2')

        with open(os.path.join(others_dir, 'config.yml'), 'w') as config:
            config.write(
                'extends: ../config.base.yml\ndebug: true\nverbose: true\nb: 5'
            )

        config_file = os.path.join(others_dir, 'other_config.yml')
        with open(config_file, 'w') as other:
            other.write('extends: config.yml\nverbose: false')

        config = configuro.load(config_filename=config_file)
        self.assertTrue(config.get('debug'))
        self.assertFalse(config.get('verbose'))
        self.assertTrue(config.get('a'), 1)
        self.assertTrue(config.get('b'), 5)

        shutil.rmtree(tmp_dir)


def test_env_prefix(tmp_path: Path):
    # Create unique file paths in the temporary directory
    base_yml = tmp_path / 'config.base.yml'
    config_yml = tmp_path / 'config.yml'

    # Write content to the base and config files
    base_yml.write_text('debug: false\nverbose: false\na: 1\nb: 2')
    config_yml.write_text('extends: config.base.yml\ndebug: true\nverbose: true\nb: 5')

    # Set the environment variable to the temporary directory
    env_prefix = 'TEST_PRFX'
    full_env_var = f'{env_prefix}_CONFIG'
    os.environ[full_env_var] = str(tmp_path / 'config.yml')

    # Load the configuration
    config = configuro.load(env_prefix=env_prefix)

    # Assertions to ensure the values are as expected
    assert config.get('debug') is True
    assert config.get('verbose') is True
    assert config.get('a') == 1
    assert config.get('b') == 5

    del os.environ[full_env_var]


class MergeFunctionTests(unittest.TestCase):
    def setUp(self):
        self.SENTINEL = INHERITANCE_SENTINEL

    def test_not_valid_iterables(self):
        with self.assertRaises(ValueError):
            # Accessed via core because merge is not part of the public API
            configuro.merge(1, 2, 3)

    def test_success(self):
        merged = configuro.merge({'a': 2}, {'b': 1})
        self.assertDictEqual(merged, {'a': 2, 'b': 1})

    def test_merge_list_start_sentinel(self):
        merged = configuro.merge({'a': [1, 2, 3]}, {'a': [self.SENTINEL, 4, 5]})
        self.assertDictEqual(merged, {'a': [1, 2, 3, 4, 5]})

    def test_merge_list_middle_sentinel(self):
        merged = configuro.merge({'a': [1, 2, 3]}, {'a': [0, self.SENTINEL, 4]})
        self.assertDictEqual(merged, {'a': [0, 1, 2, 3, 4]})

    def test_merge_list_end_sentinel(self):
        merged = configuro.merge({'a': [1, 2, 3]}, {'a': [-1, 0, self.SENTINEL]})
        self.assertDictEqual(merged, {'a': [-1, 0, 1, 2, 3]})

    def test_merge_multiple_lists_with_sentinel(self):
        merged = configuro.merge(
            {'a': [1, 2]},
            {'a': [self.SENTINEL, 3, 4]},
            {'a': [0, self.SENTINEL]},
        )
        self.assertDictEqual(merged, {'a': [0, 1, 2, 3, 4]})

    def test_merge_list_without_sentinel(self):
        merged = configuro.merge({'a': [1, 2, 3]}, {'a': [4, 5, 6]})
        self.assertDictEqual(merged, {'a': [4, 5, 6]})

    def test_merge_empty_list(self):
        merged = configuro.merge({'a': [1, 2, 3]}, {'a': []})
        self.assertDictEqual(merged, {'a': []})


class ConfigTests(unittest.TestCase):
    def test_build_no_args(self):
        config = configuro.Config.build()
        self.assertDictEqual(config._config, {})

    def test_simple_config(self):
        config = configuro.Config(a=1, b=2, c=3)
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 2)
        self.assertEqual(config.get('c'), 3)
        self.assertEqual(config.get('d'), None)

    def test_config_crazy(self):
        d1 = {'a': 1, 'b': 2, 'c': 3}
        d2 = {'a': 100, 'd': 4}
        config = configuro.Config(debug=True, **{**d1, **d2})
        self.assertEqual(config.get('a'), 100)
        self.assertEqual(config.get('b'), 2)
        self.assertEqual(config.get('c'), 3)
        self.assertEqual(config.get('d'), 4)
        self.assertEqual(config.get('debug'), True)

    def test_config_with_dict_is_config(self):
        d = {'a': 1, 'd': {'a': 2}}
        config = configuro.Config(**d)
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('d/a'), 2)

    def test_config_from_dicts(self):
        d1 = {
            'a': 1,
            'b': {'c': 2},
            'e': True,
            'f': [1, 2],
            'g': [{'true': True}],
        }
        d2 = {
            'b': {'d': 3},
            'e': False,
            'f': [2, 3, 4],
            'g': [{'false': False, 'none': None}],
            'h': [[1, 2]],
        }
        config = configuro.Config.build(dicts=[d1, d2])
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b/c'), 2)
        self.assertEqual(config.get('b/d'), 3)
        self.assertEqual(config.get('e'), False)
        self.assertEqual(config.get('f'), [2, 3, 4])
        self.assertEqual(config.get('g'), [{'false': False, 'none': None}])
        self.assertEqual(config.get('h'), [[1, 2]])

    def test_config_with_lists_and_tuples(self):
        d = {'a': [1, 2, 3], 't': (4, 3, 2)}
        config = configuro.Config(**d)
        self.assertEqual(config.get('a'), [1, 2, 3])
        self.assertEqual(config.get('t'), (4, 3, 2))

    def test_get_method(self):
        c = configuro.Config(general={'debug': False})
        self.assertFalse(c.get('general/debug', default=True))
        self.assertEqual(c.get('security/secret_key', default='asdf'), 'asdf')
        c.delimiter = ':'
        self.assertFalse(c.get('general:debug', default=True))
        c.delimiter = '>'
        self.assertEqual(c.get('security>secret_key', default=''), '')

    def test_dict_copy(self):
        c = configuro.Config(general={'debug': False}, alist=[{'a': 1}])
        self.assertEqual(type(c), configuro.Config)
        copy = c.dict_copy()
        self.assertEqual(type(copy), dict)
        self.assertEqual(type(copy['general']), dict)
        self.assertEqual(type(copy['alist']), list)
        self.assertEqual(type(copy['alist'][0]), dict)

    def test_iter(self):
        c = configuro.Config(general={'debug': False}, alist=[{'a': 1}])
        self.assertEqual(type(c), configuro.Config)
        sections = [s for s in c]
        self.assertEqual(len(sections), 2)
        self.assertTrue('general' in sections)
        self.assertTrue('alist' in sections)

    def test_items(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        for key, value in c.items():
            self.assertEqual(value, the_dict[key])

    def test_keys(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        self.assertEqual(sorted(c.keys()), sorted(the_dict.keys()))

    def test_values(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        self.assertEqual(sorted(c.values()), sorted(the_dict.values()))

    def test_get_item(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        self.assertEqual(c['a'], the_dict['a'])
        with self.assertRaises(KeyError):
            c['nothing']

    def test_get_item_sequence(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        self.assertEqual(c[('a',)], the_dict['a'])
        with self.assertRaises(KeyError):
            c[('nothing',)]

    def test_get_item_type_error(self):
        the_dict = {'a': 1, 'b': 2, 'c': 4, 'd': True}
        c = configuro.Config(**the_dict)
        with self.assertRaises(TypeError):
            c[{'non': 'sequence'}]

    def test_len(self):
        the_dict = {'a': 1}
        c = configuro.Config(**the_dict)
        self.assertEqual(len(c), 1)

    def test_instance_to_instance_equality(self):
        the_dict = {'a': {1: 2}}
        c1 = configuro.Config(**the_dict)
        c2 = configuro.Config(**the_dict)
        self.assertEqual(c1, c2)

    def test_instance_to_dict_equality(self):
        the_dict = {'a': {1: 2}}
        c = configuro.Config(**the_dict)
        self.assertEqual(c, the_dict)

    def test_instance_to_dict_copy_to_dict_equality(self):
        the_dict = {'a': {1: 2}}
        c = configuro.Config(**the_dict)
        self.assertEqual(c, c.dict_copy())
        self.assertEqual(c.dict_copy(), the_dict)

    def test_inequality(self):
        the_dict = {'a': 5}
        the_other_dict = {'b': 5}
        c1 = configuro.Config(**the_dict)
        c2 = configuro.Config(**the_other_dict)
        self.assertNotEqual(c1, c2)


class EnvYamlConfigTests(unittest.TestCase):
    def test_simple_config(self):
        config = configuro.EnvYamlConfig.build(a=1, b=2, c=3)
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 2)
        self.assertEqual(config.get('c'), 3)
        self.assertEqual(config.get('d'), None)

    @mock.patch.dict('os.environ', {'TEST_b': '1'})
    def test_build_order_init_arg_no_override(self):
        yml = NTFile('w', delete=False)
        yml.write('debug: false\nverbose: false\na: 1\nb: 2')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(
            yaml_files=yaml_files, env_prefix='test', debug=True
        )

        self.assertFalse(config.get('verbose'))
        self.assertFalse(config.get('debug'))
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 1)

    @mock.patch.dict('os.environ', {'TEST_b': '1'})
    def test_build_order_with_no_init_arg(self):
        yml = NTFile('w', delete=False)
        yml.write('debug: true\nverbose: false\na: 1\nb: 2')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(yaml_files=yaml_files, env_prefix='test')

        self.assertFalse(config.get('verbose'))
        self.assertTrue(config.get('debug'))
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 1)

    @mock.patch.dict('os.environ', {'TEST_b': '1'})
    def test_build_order_with_init_arg(self):
        yml = NTFile('w', delete=False)
        yml.write('verbose: false\na: 1\nb: 2')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(
            yaml_files=yaml_files, env_prefix='test', debug=False
        )

        self.assertFalse(config.get('verbose'))
        self.assertFalse(config.get('debug'))
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 1)

    @mock.patch.dict('os.environ', {'TEST_general__debug': 'true'})
    def test_build_nested_value_override(self):
        yml = NTFile('w', delete=False)
        yml.write('general:\n  debug: false')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(yaml_files=yaml_files, env_prefix='test')

        self.assertTrue(config.get('general/debug'))

    @mock.patch.dict('os.environ', {'TEST_b__c': '2'})
    @mock.patch.dict('os.environ', {'TEST_b__d': '3'})
    def test_build_override_dict_element(self):
        yml = NTFile('w', delete=False)
        yml.write('b:\n  c: 1\n  d: 1\n  e: 5')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(yaml_files=yaml_files, env_prefix='test')

        self.assertEqual(config.get('b/c'), 2)
        self.assertEqual(config.get('b/d'), 3)
        self.assertEqual(config.get('b/e'), 5)
        self.assertEqual(config.get('b'), {'c': 2, 'd': 3, 'e': 5})

    @mock.patch.dict('os.environ', {'TEST_b__c_d': '3'})
    def test_build_override_with_underscores(self):
        yml = NTFile('w', delete=False)
        yml.write('b:\n  c_d: 1')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(yaml_files=yaml_files, env_prefix='test')

        self.assertEqual(config.get('b/c_d'), 3)

    @mock.patch.dict('os.environ', {'TEST_c__0': 'b'})
    def test_build_override_array(self):
        yml = NTFile('w', delete=False)
        yml.write('debug: false\nverbose: false\na: 1\nc: ["a"]')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(
            yaml_files=yaml_files, env_prefix='test', debug=True
        )

        self.assertFalse(config.get('verbose'))
        self.assertFalse(config.get('debug'))
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('c/0'), 'b')
        self.assertEqual(config.get('c'), ['b'])

    @mock.patch.dict('os.environ', {'TEST_c__0': 'b'})
    def test_build_override_array_index_errors(self):
        yml = NTFile('w', delete=False)
        yml.write('debug: false\nverbose: false\na: 1\nc: ["a"]')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(
            yaml_files=yaml_files, env_prefix='test', debug=True
        )
        default = 'random_default'
        self.assertFalse(config.get('verbose'))
        self.assertFalse(config.get('debug'))
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('c/1', default), default)
        self.assertRaises(IndexError, itemgetter('c/1'), config)
        self.assertEqual(config.get('c'), ['b'])

    @mock.patch.dict('os.environ', {'TEST_debug': 'true'})
    def test_build_env_bool(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', debug=False)
        self.assertTrue(config.get('debug') is True)

    @mock.patch.dict('os.environ', {'TEST_val': 'GEORGE'})
    def test_build_env_str(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', val='blah')
        self.assertEqual(config.get('val'), 'GEORGE')

    @mock.patch.dict('os.environ', {'TEST_val': '314'})
    def test_build_env_int(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', val=23)
        self.assertEqual(config.get('val'), 314)

    @mock.patch.dict('os.environ', {'TEST_val': '["a.b.c", "b.c.d"]'})
    def test_build_env_list(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', val=['lhost'])
        self.assertEqual(config.get('val'), ['a.b.c', 'b.c.d'])

    @mock.patch.dict('os.environ', {'TEST_val': '{"a": 1, "b": false}'})
    def test_build_env_dict(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', val={'c': 2})
        self.assertEqual(config.get('val'), {'a': 1, 'b': False})

    @mock.patch.dict('os.environ', {'TEST_val': 'a:\n  c: ["b"]'})
    def test_build_env_yaml_dict(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', val={'c': 2})
        self.assertEqual(config.get('val'), {'a': {'c': ['b']}})

    @mock.patch.dict('os.environ', {'TEST_mylist__0': '0'})
    def test_build_override_index(self):
        yml = NTFile('w', delete=False)
        yml.write('mylist:\n  - 1\n  - 2\n')
        yml.close()

        yaml_files = [yml.name]
        config = configuro.EnvYamlConfig.build(yaml_files=yaml_files, env_prefix='TEST')
        self.assertEqual(config.get('mylist'), [0, 2])

    @mock.patch.dict('os.environ', {'TEST_debug': 'GEORGE'})
    def test_build_env_ignored_if_not_present(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test')
        self.assertEqual(config.get('debug'), None)
        self.assertEqual(config.environ, {'TEST_debug': 'GEORGE'})

    @mock.patch.dict('os.environ', {'TEST_django__databases__default': 'GEORGE'})
    def test_build_env_ignored_deeper(self):
        config = configuro.EnvYamlConfig.build(env_prefix='test', django={})
        self.assertEqual(config.get('django/databases/default'), None)
        self.assertEqual(config.environ, {'TEST_django__databases__default': 'GEORGE'})

    @mock.patch.dict('os.environ', {'TEST_django__databases__default': 'GEORGE'})
    def test_build_same_case(self):
        dj_dict = {'databases': {'default': 'HENRY'}}
        config = configuro.EnvYamlConfig.build(env_prefix='test', django=dj_dict)
        self.assertEqual(config.get('django/databases/default'), 'GEORGE')
        self.assertEqual(config.environ, {'TEST_django__databases__default': 'GEORGE'})

    @mock.patch.dict('os.environ', {'TEST_DJANGO__DATABASES__DEFAULT': 'GEORGE'})
    def test_build_different_case(self):
        dj_dict = {'databases': {'default': 'HENRY'}}
        config = configuro.EnvYamlConfig.build(env_prefix='test', django=dj_dict)
        self.assertEqual(config.get('django/databases/default'), 'HENRY')
        self.assertNotEqual(
            config.environ, {'TEST_django__databases__default': 'GEORGE'}
        )


class YamlConfigTests(unittest.TestCase):
    def test_config_from_yaml_string(self):
        yml = 'a: 1\nb: 2'
        config = configuro.YamlConfig.build(yaml_str=yml)
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 2)

    def test_config_from_yaml_string_with_regex(self):
        yml = 'file_pattern: apl{ee|aw}[0-9]+\\.out'
        config = configuro.YamlConfig.build(yaml_str=yml)
        self.assertEqual(config.get('file_pattern'), r'apl{ee|aw}[0-9]+\.out')

    def test_config_from_yaml_string_with_regex_with_quotes(self):
        yml = "file_pattern: 'apl{ee|aw}[0-9]+\\.out'"
        config = configuro.YamlConfig.build(yaml_str=yml)
        self.assertEqual(config.get('file_pattern'), r'apl{ee|aw}[0-9]+\.out')

    def test_from_yaml_files(self):
        yml = NTFile('w', delete=False)
        yml.write('a: 1\nb: 2')
        yml.close()

        config = configuro.YamlConfig.build(yaml_files=[yml.name])
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 2)

    def test_from_yaml_files_bad_yaml(self):
        yml = NTFile('w', delete=False)
        yml.write('a: ][\nb:2')
        yml.close()
        from yaml.parser import ParserError

        self.assertRaises(
            ParserError, configuro.YamlConfig.build, yaml_files=[yml.name]
        )

    def test_build_all(self):
        yml = NTFile('w', delete=False)
        yml.write('a: 1\nb: 2')
        yml.close()

        config = configuro.YamlConfig.build(
            yaml_files=[yml.name], dicts=[{'a': 2}], a=None
        )
        self.assertEqual(config.get('a'), 1)

    def test_config_from_yaml_files_list_inheritance(self):
        with NTFile('w') as ymlparent, NTFile('w') as ymlchild:
            ymlparent.write('a:\n  - 1\n  - 2')
            ymlparent.flush()
            os.fsync(ymlparent.fileno())

            ymlchild.write('a:\n  - ...\n  - 3')
            ymlchild.flush()
            os.fsync(ymlchild.fileno())

            config = configuro.YamlConfig.build(
                yaml_files=[ymlparent.name, ymlchild.name]
            )
        self.assertEqual(config.get('a'), [1, 2, 3])

    def test_config_from_yaml_files_empty_list(self):
        with NTFile('w') as ymlparent, NTFile('w') as ymlchild:
            ymlparent.write('a:\n  - 1\n  - 2')
            ymlparent.flush()
            os.fsync(ymlparent.fileno())

            ymlchild.write('a: []')
            ymlchild.flush()
            os.fsync(ymlchild.fileno())

            config = configuro.YamlConfig.build(
                yaml_files=[ymlparent.name, ymlchild.name]
            )
        self.assertEqual(config.get('a'), [])

    def test_config_from_yaml_files_empty_values(self):
        with NTFile('w') as ymlparent, NTFile('w') as ymlchild:
            ymlparent.write(
                'a: 1\n'
                'b: 2\n'
                'c: 3\n'
                'd:'  # empty detection shouldn't prevent future override
            )
            ymlparent.flush()
            os.fsync(ymlparent.fileno())
            ymlchild.write(
                'a: #10\nb:\nc: null\nd: 4'  # ten is commented out
            )
            ymlchild.flush()
            os.fsync(ymlchild.fileno())

            config = configuro.YamlConfig.build(
                yaml_files=[ymlparent.name, ymlchild.name]
            )
            self.assertEqual(config.get('a'), 1)
            self.assertEqual(config.get('b'), 2)
            self.assertEqual(config.get('c'), 3)
            self.assertEqual(config.get('d'), 4)

    def test_config_from_yaml_files_empty_dict_override(self):
        with NTFile('w') as ymlparent, NTFile('w') as ymlchild:
            ymlparent.write("a: {'aa': 1}")
            ymlparent.flush()
            os.fsync(ymlparent.fileno())
            ymlchild.write('a: {}')
            ymlchild.flush()
            os.fsync(ymlchild.fileno())

            config = configuro.YamlConfig.build(
                yaml_files=[ymlparent.name, ymlchild.name]
            )
            self.assertEqual(config.get('a'), {})
