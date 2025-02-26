from setuptools import setup, find_packages
import pathlib

NAME = "svgl"
GITHUB = "tsnaketech"

parent = pathlib.Path(__file__).parent.resolve()
license = (parent / 'LICENSE').read_text(encoding='utf-8')
version = (parent / 'VERSION').read_text(encoding='utf-8')
long_description = (parent / 'README.md').read_text(encoding='utf-8')

setup(
    name=NAME,
    version=version,
    description='Interact with the https://svgl.app/.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/{0}/{1}'.format(GITHUB, NAME),
    author='SnakeTech',
    author_email='repo@snaketech.net',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'httpx',
        'pydantic'
    ],
    project_urls={
        'Source': 'https://github.com/{0}/{1}'.format(GITHUB, NAME),
        'Issues': 'https://github.com/{0}/{1}/issues'.format(GITHUB, NAME)
    },

    # https://pypi.org/classifiers/
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",
        "Natural Language :: French",
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)