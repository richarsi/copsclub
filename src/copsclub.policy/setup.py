from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='copsclub.policy',
      version=version,
      description="COPS Policy",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Simon Richardson',
      author_email='claretnbluester@gmail.com',
      url='http://www.copsclub.co.uk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['copsclub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'copsclub.theme',
          'copsclub.content',
          'Products.Doormat',
          'myswimmingclub.theme',
          'collective.embedly',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test' : ['plone.app.testing',]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      # setup_requires=["PasteScript"],
      # paster_plugins=["ZopeSkel"],
      )
