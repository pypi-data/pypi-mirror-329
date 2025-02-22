# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filecloudapi', 'filecloudapi.tests']

package_data = \
{'': ['*']}

install_requires = \
['click', 'requests']

setup_kwargs = {
    'name': 'filecloudapi-python',
    'version': '0.4.0',
    'description': 'A Python library to connect to a Filecloud server',
    'long_description': '# Overview\n\nA Python library to connect to a Filecloud server\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Linux Build](https://img.shields.io/github/actions/workflow/status/codelathe/template-python-demo/main.yml?branch=main&label=linux)](https://github.com/codelathe/filecloudapi-python/actions)\n[![Windows Build](https://img.shields.io/appveyor/ci/codelathe/template-python-demo/main.svg?label=windows)](https://ci.appveyor.com/project/codelathe/filecloudapi-python)\n[![Code Coverage](https://img.shields.io/codecov/c/github/codelathe/filecloudapi-python)\n](https://codecov.io/gh/codelathe/filecloudapi-python)\n[![Code Quality](https://img.shields.io/scrutinizer/g/codelathe/filecloudapi-python.svg?label=quality)](https://scrutinizer-ci.com/g/codelathe/filecloudapi-python/?branch=main)\n[![PyPI License](https://img.shields.io/pypi/l/filecloudapi-python.svg)](https://pypi.org/project/filecloudapi-python)\n[![PyPI Version](https://img.shields.io/pypi/v/filecloudapi-python.svg?label=version)](https://pypi.org/project/filecloudapi-python)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/filecloudapi-python.svg?color=orange)](https://pypistats.org/packages/filecloudapi-python)\n\n## Setup\n\n### Requirements\n\n* Python 3.11+\n\n### Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install filecloudapi-python\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add filecloudapi-python\n```\n\n## Usage\n\nAfter installation, the package can be imported:\n\n```text\n$ python\n>>> import filecloudapi\n>>> filecloudapi.__version__\n```\n',
    'author': 'FileCloud',
    'author_email': 'dev@filecloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/filecloudapi-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
