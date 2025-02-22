# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioplumber']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=8.1.5,<9.0.0',
 'pandas>=2.2.3,<3.0.0',
 'requests>=2.32.3,<3.0.0',
 'rich>=13.8.1,<14.0.0',
 'textual[syntax]==1.0.0']

entry_points = \
{'console_scripts': ['pipit = bioplumber.tui:main']}

setup_kwargs = {
    'name': 'bioplumber',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'ParsaGhadermazi',
    'author_email': '54489047+ParsaGhadermazi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
