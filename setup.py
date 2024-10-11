#!/usr/bin/env python
from setuptools import setup


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


tests_require = [
    'pytest',
]

setup(
    name='blurhash-python',
    description='BlurHash encoder implementation for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://blurha.sh',
    use_scm_version=dict(
        write_to='src/blurhash/_version.py',
    ),
    author='Atte Lautanala',
    author_email='atte.lautanala@wolt.com',
    packages=['blurhash'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi',
        'Pillow',
    ],
    setup_requires=[
        'cffi',
        'setuptools-scm',
    ],
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
