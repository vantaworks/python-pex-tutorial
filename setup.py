import os
from babble import __version__
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md') as r:
	long_description = r.read()

setup(name='babble',
	  py_modules=['babble'],
	  version=__version__,
	  author="Robert Rice",
	  author_email="h4110w33n@gmail.com",
	  description='A Python Pex Demo with Flask and Gunicorn.',
      long_description=long_description,
	  long_description_content_type='text/markdown',
	  keywords=['pex', 'gunicorn', 'flask', 'deployment', 'demo'],
	  classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Information Technology',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	install_requires=required,
	provides=['babble'],
	license='GNU General Public License v3 (GPLv3)',
	packages=['babble'],
)


