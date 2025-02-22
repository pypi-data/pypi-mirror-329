#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __file__: setup.py
# __author__: qinghua.yao
# __date__: 2025/2/21
# __description__:
import io
import os
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command

about = {
    'title': 'MarkdownToXmind',
    'description': '将Markdown文本格式内容转换为较新版本XMind思维导图',
    'keywords': 'MarkdownToXmind, xmind',
    'url': 'https://gitee.com/seamam/markdown-to-xmind.git',
    'author': 'QingHua.Yao',
    'email': 'yaohua1179@163.com',
    'version': '1.0.1'
}

here = os.path.abspath(os.path.dirname(__file__))
with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

install_requires = []


class PyPiCommand(Command):
    """ Build and publish this package and make a tag.
        Support: python setup.py pypi
        Copied from requests_html
    """
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in green color."""
        print('\033[0;32m{0}\033[0m'.format(s))

    def initialize_options(self):
        """ override
        """
        pass

    def finalize_options(self):
        """ override
        """
        pass

    def run(self):
        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        self.status('Publishing git tags...')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        try:
            self.status('Removing current build artifacts...')
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'build'))
            rmtree(os.path.join(here, 'XMind.egg-info'))
        except OSError:
            pass

        self.status('Congratulations! Upload PyPi and publish git tag successfully...')
        sys.exit()


setup(
    name=about['title'],
    description=about['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=about['keywords'],
    author=about['author'],
    author_email=about['email'],
    url=about['url'],
    version=about['version'],
    license='Apache License',
    packages=find_packages(exclude=['example', 'tests', 'test.*', 'docs']),
    package_data={'': ['README.md']},
    install_requires=install_requires,
    extras_require={},
    python_requires='>=3.9, <4',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        # python3 setup.py pypi
        'pypi': PyPiCommand
    }
)
