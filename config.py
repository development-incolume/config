#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '@britodfbr'

import ast
import configparser
import json
import toml
import yaml
import incolumepy.config


incolumepy.config.run()

print("# read config toml")
config = toml.load('settings/config.toml')
print(f"{config=}")
print(f'{config.get("project").get("author")}')
print(f'{config["project"]["author"]}')
print(f"{config['sqlite']['dev']['file']}")

print("\n\n# read config yaml")
with open('settings/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
print(f"{config=}")
print(f'{config.get("project").get("author")}')
print(f'{config["project"]["author"]}')
print(f"{config['sqlite']['dev']['file']}")

print("\n\n# read config json")
with open('settings/config.json') as f:
    config = json.load(f)
print(f"{config=}")
print(f'{config.get("project").get("author")}')
print(f'{config["project"]["author"]}')
print(f"{config['sqlite']['dev']['file']}")

print("\n\n# read config ini")
parser = configparser.ConfigParser()
parser.read('settings/config.ini')
config = parser.__dict__['_sections']
print(f"{config=}")
print(f'{config.get("project").get("author")}')
print(f'{config["project"]["author"]}')
# converte str para dict
print(f"{ast.literal_eval(config.get('sqlite').get('dev')).get('file')}")

print("\n\n# read config cfg")
parser = configparser.ConfigParser()
parser.read('settings/config.cfg')
config = {section: dict(parser.items(section)) for section in parser.sections()}
print(f"{config=}")
print(f'{config.get("project").get("author")}')
print(f'{config["project"]["author"]}')
# converte str para dict
print(f"{ast.literal_eval(config.get('sqlite').get('dev')).get('file')}")
