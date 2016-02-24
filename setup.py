from setuptools import setup, find_packages

setup(name='robust_graph',
      version='1.0',
      description='Graph Robustness Library',
      author='Yoshiki Satotani',
      author_email='yoshikimethod@hotmail.co.jp',
      packages=find_packages(),
      install_requires=['networkx'],
      )
