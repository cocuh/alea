from setuptools import find_packages, setup

install_requires = [
    'requests',
    'numpy',
    'tqdm',
    'filelock',
    'scipy',
]
tests_require = [
    'nose',
    'coverage',
]

setup(
  name='alea',
  version='0.0.1',
  packages=find_packages(exclude=['tests']),
  url='',
  license='Apache v2',
  install_requires=install_requires,
  tests_require=tests_require,
  extras_require={
    'test': tests_require,
  },
  author='cocuh',
  author_email='',
  description='',
)
