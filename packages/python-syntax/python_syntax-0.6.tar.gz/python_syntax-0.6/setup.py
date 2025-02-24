# name same as folder Name

from setuptools import setup, find_packages

setup(
	name="python_syntax",
	version="0.6",
	packages=find_packages(),
	install_requires=[

	],
	entry_points={

		"console_scripts":[
			"python_syntax = python_syntax.main:main",
			


		],
	},
)
# python setup.py sdist bdist_wheel