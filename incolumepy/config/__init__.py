#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '@britodfbr'

from abc import ABC
from pathlib import Path
import abc
import toml
import configparser
import json
import yaml


__package__ = Path(__file__).parent.parent.parent
assert __package__.is_dir(), f"{__package__}"


class Settings(metaclass=abc.ABCMeta):
    def __init__(self, filename):
        self.filename = filename
        self.content = ""

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        value = Path(value)
        assert value.is_file(), f"Arquivo inexistente {value}"
        self.__filename = value

    @abc.abstractmethod
    def read(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_json(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_ini(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_toml(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_yaml(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError


class SettingsToml(Settings, ABC):
    def __init__(self, filename):
        assert filename.name.endswith('.toml')
        super().__init__(filename)

    def read(self):
        self.content = toml.load(self.filename)

    def to_dict(self):
        self.read()
        return self.content

    def to_ini(self):
        config = configparser.ConfigParser()
        config.read_dict(self.to_dict())
        with self.filename.with_suffix('.ini').open('w') as configfile:
            config.write(configfile)
        return True

    def to_json(self):
        with self.filename.with_suffix('.json').open('w') as file:
            json.dump(self.content, file, indent=4)
        return True

    def to_toml(self):
        return False

    def to_yaml(self):
        with self.filename.with_suffix('.yaml').open('w') as file:
            yaml.dump(self.content, file)


if __name__ == '__main__':
    o = SettingsToml(__package__ / 'settings/config.toml')
    o.read()
    o.to_ini()
    o.to_json()
    o.to_yaml()
    print(o.content)
