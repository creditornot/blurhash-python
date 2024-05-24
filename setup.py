from setuptools import setup

setup(
    cffi_modules=['src/build_blurhash.py:ffibuilder'],
)
