from pathlib import Path
from setuptools import setup

setup(
    name='python-heptapod-runner',
    version='0.8.0',
    author='Georges Racinet',
    author_email='georges.racinet@cloudcrane.io',
    url='https://foss.heptapod.net/heptapod/heptapod-paas-runner',
    description="Deprecated (renamed) Heptapod Runner: Python utilities and subsystems",
    long_description=("This project has been renamed and superseded "
                      "by `heptapod-paas-runner`. Please install the latter instead."),
    long_description_content_type="text/markdown",
    keywords='hg mercurial git heptapod gitlab',
    license='GPLv3+',
    # do not use find_packages, as it could recurse into the Git and
    # Mercurial repositories
    install_requires=['heptapod-paas-runner']
)
