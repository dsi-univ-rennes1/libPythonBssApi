from setuptools import setup

setup(
    name='lib_Partage_BSS',
    version='2.2.1',
    packages=['lib_Partage_BSS',
              'lib_Partage_BSS.utils', 'lib_Partage_BSS.exceptions', 'lib_Partage_BSS.models','lib_Partage_BSS.services',
              ],
    url='https://gitlab.univ-rennes1.fr/57NUM/libPythonBssApi',
    license='',
    author='rpeillet',
    author_email='',
    description='Bibliothèque permettant l\'intégoration de l\'API BSS PAratage de RENATER',
    install_requires=['xmljson', 'requests','pytest','pytest-mock']
)
