from setuptools import setup, find_packages

setup(name='robust_graph',
      version='0.1.0',
      description='Graph Robustness Library',
      author='arity-r',
      author_email='yoshikimethod@hotmail.co.jp',
      packages=['robust_graph', 'robust_graph.algorithms'],
      include_package_data=True,
      package_data={'robust_graph': ['USAir97.txt']},
      install_requires=['networkx'],
      )

