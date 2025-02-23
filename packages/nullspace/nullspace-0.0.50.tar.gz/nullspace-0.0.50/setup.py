from os import path
from setuptools import setup, find_packages, Extension
import sys
import versioneer
from Cython.Build import cythonize
import numpy


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 6)
if sys.version_info < min_version:
    error = """
nullspace does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

setup(
    name='nullspace',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python package for doing science.",
    long_description=readme,
    author="G",
    author_email='abc@outlook.com',
    url='https://github.com/ke-zhang-rd/nullspace',
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            # 'command = some.module:some_function',
        ],
    },
    include_package_data=True,
    package_data={
        'nullspace.svd_wrapper': ["nullspace/include/svd.h", "nullspace/python/svd_wrapper.pyx"]
        # When adding files here, remember to update MANIFEST.in as well,
        # or else they will not be included in the distribution on PyPI!
        # 'path/to/data_file',
    },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    include_dirs=[numpy.get_include()],
    ext_modules=cythonize(Extension("nullspace.svd_wrapper",
                                    sources=["nullspace/python/svd_wrapper.pyx"],
                                    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
                                    include_dirs=[numpy.get_include(), "nullspace/include", "nullspace"],
                                    # Based on suggestion on
                                    # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiling-with-the-cythonize-command
                                    language="c++")),
)
