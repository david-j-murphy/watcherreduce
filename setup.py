from setuptools import setup

setup(	name='watcherreduce',
		version='0.1',
		description='Tools for interacting with the Watcher Data Repo.',
		author='David Murphy',
		author_email='david@spacescience.ie',
		packages=['watcherreduce'],
		install_requires=['astropy','numpy'],
		scripts=['bin/wreduce-folder'],
		zip_safe=False
		)
