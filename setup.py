from setuptools import setup

setup(
    name='lib_Partage_BSS',
    version='1.0.0',
    packages=['doc', 'test_unitaire',
              'lib_Partage_BSS',
              'lib_Partage_BSS.utils', 'lib_Partage_BSS.exceptions', 'lib_Partage_BSS.models','lib_Partage_BSS.services',
              ],
    url='https://gitlab.univ-rennes1.fr/57NUM/libPythonBssApi',
    license='',
    author='rpeillet',
    author_email='',
    description='Bibliothèque permettant l\'intégoration de l\'API BSS PAratage de RENATER',
    install_requires=['xmljson', 'requests']
)
