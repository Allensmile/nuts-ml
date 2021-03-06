"""
.. module:: config
   :synopsis: Handling of configuration files.
"""

import os
import yaml
import json


class Config(dict):
    """
    Dictionary that allows access via keys or attributes.

    Used to store and access configuration data.
    """

    def __init__(self, *args, **kwargs):
        """
        Create dictionary.

        >>> contact = Config({'age':13, 'name':'stefan'})
        >>> contact['age']
        13

        >>> contact.name
        'stefan'

        >>> contact.surname = 'maetschke'
        >>> contact.surname
        'maetschke'

        :param args args: See dict
        :param kwargs kwargs: See dict
        """
        super(Config, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def isjson(filepath):
        """
        Return true if filepath ends with '.json'.

        :param str filepath: Filepaht
        :return: True if filepath points ot JSON file.
        :rtype: bool
        """
        return filepath.lower().endswith('.json')

    def load(self, filepath):
        """
        Load configuration from file in JSON or YAML format.

        >>> cfg = Config().load('tests/data/configuration.json')
        >>> cfg.number
        13

        :param str filepath: Path to JSON or YAML file.
        :return: returns loaded configuration.
        :rtype: Config
        """
        reader = json.load if Config.isjson(filepath) else yaml.load
        with open(filepath, 'r') as f:
            self.__init__(reader(f))
        return self

    def save(self, filepath):
        """
        Save configuration to file in JSON or YAML format.

        >>> cfg = Config({'number': 13, 'name': 'Stefan'})
        >>> cfg.save('tests/data/configuration.yaml')

        :param str filepath: Filepath. Should end with '.json' or '.yaml'
        """
        writer = json.dump if Config.isjson(filepath) else yaml.dump
        with open(filepath, 'w') as f:
            writer(dict(self), f)


def load_config(filename):
    """
    Load configuration file in YAML format from locations in defined order.

    The search order for the config file is:
    1) user home dir
    2) current dir
    3) full path
    
    |  Example file: 'tests/data/config.yaml'
    |  filepath : c:/Maet
    |  imagesize : [100, 200]

    >>> cfg = load_config('tests/data/config.yaml')
    >>> cfg.filepath
    'c:/Maet'

    >>> cfg['imagesize']
    [100, 200]

    :param filename: Name or full path of configuration file.
    :return: dictionary with config data. Note that config data can be
             accessed by key or attribute, e.g. cfg.filepath or cfg.['filepath']
    :rtype: ConfigDict
    """
    filepaths = []
    for dirpath in os.path.expanduser('~'), os.curdir, '':
        try:
            filepath = os.path.join(dirpath, filename)
            filepaths.append(filepath)
            with open(filepath, 'r') as f:
                return Config(yaml.load(f))
        except IOError:
            pass
    raise IOError('Configuration file not found: ' + ', '.join(filepaths))
