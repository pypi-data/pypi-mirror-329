from setuptools import setup, find_packages
import pathlib

__version__ = "0.0.2"

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='web_maya',
    version=__version__,

    url='https://github.com/Vladislavus1/Maya',
    author='Vladislavus1',
    author_email='vlydgames@gmail.com',

    description='Mini web-framework package that provides basic web-programming features.',
    long_description=README,
    long_description_content_type='text/markdown',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jinja2==3.1.3',
        'colorama==0.4.6'
    ],
)