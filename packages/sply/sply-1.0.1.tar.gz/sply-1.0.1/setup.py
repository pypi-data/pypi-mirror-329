# -*- coding: utf-8 -*-
from setuptools import setup

packages = ['sply', 'sply/overmind']

package_data = {'': ['*']}

setup_kwargs = {
    'name': 'sply',
    'version': '1.0.1',
    'description': 'a bridge between real and simulated python interpreters',
    'long_description': '',
    'author': 'Richard Benson',
    'author_email': 'richardbenson91477@protonmail.com',
    'maintainer': 'Richard Benson',
    'maintainer_email': 'richardbenson91477@protonmail.com',
    'url': 'https://github.com/richardbenson91477/sply',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
    'scripts': ['bin/sply_chat_interact.py']
}

setup(**setup_kwargs)

