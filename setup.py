from setuptools import setup, find_packages

setup(
    name='Omini',
    version='0.0.1',
    packages=find_packages(),
    license="",
    install_requires=[
        'exceptiongroup>=1.1.2',
        'iniconfig>=2.0.0',
        'packaging>=23.1',
        'pluggy>=1.2.0',
        'pygdbmi>=0.11.0.0',
        'tomli>=2.0.1'
    ],
    package_data={'Omini': [
        'tests/unit_tests/gdb_responses/*.*', 'tox.ini', 'README.md', 'LICENSE']},
    author='Erick Setubal Bacurau',
    author_email='your@email.com',
    description='A Framework for Integration Testing in Embedded Systems',
    url='https://github.com/Notua-Sistemas-Embarcados/Omini',
)
