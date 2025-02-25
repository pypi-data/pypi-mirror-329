from setuptools import setup, find_packages

setup(
    name="insider_scripts",
    version="1.0",
    py_modules=["insider_scripts"],
    maintainer="Sébastien Gachoud",
    maintainer_email="sebastien.gachoud@gmail.com",
    description="Run python scripts from inside a package without relative import error.",
    long_description=open('readme.md').read()
)