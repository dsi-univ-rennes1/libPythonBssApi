import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lib_Partage_BSS-univ-rennes',
    version='2.3.4',
    author='DSI Univ Rennes1',
    author_email='',
    description="Bibliothèque permettant l'interrogation de l'API BSS Partage de RENATER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dsi-univ-rennes1/libPythonBssApi',
    packages=setuptools.find_packages(),
    install_requires=['xmljson', 'requests', 'wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: French",
    ],
    scripts=['cli-bss.py'],
    python_requires='>=3.5',
)
