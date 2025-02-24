# # name same as folder Name

# from setuptools import setup, find_packages

# setup(
# 	name="python_syntax",
# 	version="0.7",
# 	packages=find_packages(),
# 	install_requires=[

# 	],
# 	entry_points={

# 		"console_scripts":[
# 			"python_syntax = python_syntax.main:main",
			


# 		],
# 	},
# )
# python setup.py sdist bdist_wheel

from setuptools import setup, find_packages

setup(
    name='python_syntax',
    version='0.9',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    entry_points={
        "console_scripts": [
            "python_syntax = python_syntax.main:main",  # Command-line interface entry point
        ]
    },
    author="Sandeepan Mohanty",
    author_email="sandimohanty@gmail.com",
    description="A CLI tool to insert common Python syntax into files.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python_syntax",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
