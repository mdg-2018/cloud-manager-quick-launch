from setuptools import *

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()
with open("version.txt", "r") as fh:
    vers = fh.read().splitlines()[0]

setup(
	name='SpawnHub',
	version=vers,
	py_modules=['SpawnHub'],
	packages=find_packages(),
	install_requires=required,
	author="graboskyc",
	author_email="chris@grabosky.net",
	description="Python and Blazor app to handle deploying a rep set and connect to CM on demand.",
)