from setuptools import setup, find_packages

setup(
  name='alea',
  version='0.0.1',
  packages=find_packages(exclude=['tests']),
  url='',
  license='Apache v2',
  install_requires=[
    'requests',
    'numpy',
    'tqdm',
    'filelock',
    'scipy',
  ],
  tests_require=[
    'nose',
    'coverage',
  ],
  author='cocuh',
  author_email='',
  description='',
)
