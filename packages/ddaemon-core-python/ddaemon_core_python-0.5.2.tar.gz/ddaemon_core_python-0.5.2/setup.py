"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import os
import re

from os import path
from setuptools import (
    find_packages,
    setup)


PROJECT_PATH = path.abspath(path.dirname(__file__))
VERSION_RE = re.compile(r"""__version__ = [""]([0-9.]+((dev|rc|b)[0-9]+)?)[""]""")


with open(os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8") as readme:
    README = readme.read()


def get_version():
    """Get Version."""
    with open(path.join(PROJECT_PATH, "ddcore", "__init__.py"), encoding="utf-8") as version:
        init = version.read()

        return VERSION_RE.search(init).group(1)


# -----------------------------------------------------------------------------
# --- Allow `setup.py` to be run from any Path.
# -----------------------------------------------------------------------------
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="ddaemon-core-python",
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3 License",
    description="DDaemon Core.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/asuvorov/ddaemon-core-python/",
    author="Artem Suvorov",
    author_email="artem.suvorov@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # "License-Expression: GPL-3.0",
        # "License-File: LICENSE",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Security",
    ],
    install_requires=[
        "Django==4.2.13",
        "boto3==1.34.122",
        "beautifulsoup4==4.12.3",
        "bumpversion==0.6.0",
        "coverage==7.5.0",
        "django-annoying==0.10.6",
        "django-ckeditor==6.7.1",
        "django-countries==7.6.1",
        "django-extensions==3.2.3",
        "django-ipware==4.0.2",
        # "django-papertrail==1.1.9",
        "django-phonenumbers==1.0.1",
        "django-phonenumber-field==7.3.0",
        "django-storages==1.14.3",
        "geoip2>=3.0.0",
        # "gitchangelog==3.0.4",
        "ipython==8.18.1",
        "json-log-formatter==1.1",
        "mysqlclient==2.2.4",
        "pendulum==3.0.0",
        "pep257==0.7.0",
        "pep8==1.7.1",
        # "psycopg2-binary==2.9.5",
        "pycodestyle==2.11.1",
        "pydocstyle==6.3.0",
        "pyflakes==3.2.0",
        "pylint==3.1.0",
        "pylint-django==2.5.5",
        "pymemcache==4.0.0",
        "pytest==7.4.0",
        "pytz==2024.1",
        "pyyaml==6.0.1",
        "python-decouple==3.8",
        "python-memcached==1.62",
        "requests==2.31.0",
        "simplejson==3.19.2",
        "termcolor==2.4.0",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
)
