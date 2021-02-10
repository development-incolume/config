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


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


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


class SettingsMigrate(Settings, ABC):
    def __init__(self, filename, output=None):
        super().__init__(filename)
        self.output = output

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        if value:
            value = Path(value)
            value.parent.mkdir(exist_ok=True)
        self.__output = value

    def read(self):
        if self.filename.name.endswith('.toml'):
            self.content = toml.load(self.filename)

        if self.filename.name.endswith('.json'):
            with self.filename.open() as f:
                self.content = json.load(f)

        if self.filename.name.endswith('.yaml'):
            with self.filename.open() as f:
                self.content = yaml.load(f, Loader=yaml.FullLoader)

        if self.filename.name.endswith('.ini') or self.filename.name.endswith('.cfg'):
            # # https://stackoverflow.com/a/3220891/5132101
            # config = MyParser()
            # config.read(self.filename)
            # self.content = config.as_dict()

            # config = configparser.ConfigParser()
            # config.read(self.filename)
            # # https://stackoverflow.com/a/3220740/5132101
            # dictionary = {}
            # for section in config.sections():
            #     dictionary[section] = {}
            #     for option in config.options(section):
            #         dictionary[section][option] = config.get(section, option)
            # self.content = dictionary

            # config = configparser.ConfigParser()
            # config.read(self.filename)
            # # https://stackoverflow.com/a/36547478/5132101
            # self.content = {section: dict(config.items(section)) for section in config.sections()}

            config = configparser.ConfigParser()
            config.read(self.filename)
            # https://stackoverflow.com/a/3220887/5132101
            self.content = config.__dict__['_sections']

    def to_dict(self):
        self.read()
        return self.content

    def to_cfg(self):
        config = configparser.ConfigParser()
        config.read_dict(self.to_dict())
        output = self.output.with_suffix('.cfg') if self.output else self.filename.with_suffix('.cfg')
        try:
            with output.open('x') as file:
                config.write(file)
            return True
        except FileExistsError:
            pass

    def to_ini(self):
        config = configparser.ConfigParser()
        config.read_dict(self.to_dict())
        output = self.output.with_suffix('.ini') if self.output else self.filename.with_suffix('.ini')
        try:
            with output.open('x') as file:
                config.write(file)
            return True
        except FileExistsError:
            pass

    def to_json(self):
        output = self.output.with_suffix('.json') if self.output else self.filename.with_suffix('.json')
        try:
            with output.open('x') as file:
                json.dump(self.content, file, indent=4)
            return True
        except FileExistsError:
            pass

    def to_toml(self):
        output = self.output.with_suffix('.toml') if self.output else self.filename.with_suffix('.toml')
        try:
            with output.open('x') as file:
                toml.dump(self.content, file)
            return True
        except FileExistsError:
            pass

    def to_yaml(self):
        output = self.output.with_suffix('.yaml') if self.output else self.filename.with_suffix('.yaml')
        try:
            with output.open('x') as file:
                yaml.dump(self.content, file)
        except FileExistsError:
            pass


def run():
    n = SettingsMigrate(__package__ / 'settings/config.toml')
    n.to_cfg()
    n.to_ini()
    n.to_json()
    n.to_toml()
    n.to_yaml()


if __name__ == '__main__':
    run()
    o = SettingsMigrate(__package__ / 'settings/config.json', __package__ / 'output/output_from_json.txt')
    o.read()
    print(o.content)
    o.to_cfg()
    o.to_ini()
    o.to_json()
    o.to_toml()
    o.to_yaml()
