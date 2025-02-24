# name same as folder Name

from setuptools import setup, find_packages

setup(
	name="python_syntax",
	version="0.2",
	packages=find_packages(),
	install_requires=[

	],
	entry_points={

		"console_scripts":[
			"hello=python_syntax:hello",
        "test=python_syntax:test",
	"bye=python_syntax:bye",


		],
	},
)
#python setup.py sdist bdist_wheel