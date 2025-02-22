from setuptools import setup, find_packages
import pathlib

__version__ = "0.0.1"

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='maya-framework',
    version=__version__,

    url='https://github.com/Vladislavus1/Maya',
    author='Vladislavus1',
    author_email='vlydgames@gmail.com',

    description='Mini web-frame work package that provides basic web-programming features.',
    long_description=README,
    long_description_content_type='text/markdown',

    packages=find_packages(),
    install_requires=[
        'jinja2==3.1.3',
        'colorama==0.4.6'
    ],
)