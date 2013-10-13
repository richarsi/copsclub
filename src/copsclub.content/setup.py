from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='copsclub.content',
      version=version,
      description="Installation package for swimming club content, such as Squads, Locations and Swimming Meets.",
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
      url='http://www.copsclub.co.uk/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['copsclub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.dexterity [grok]',
          'plone.app.referenceablebehavior',
          'plone.app.relationfield',
          'plone.namedfile [blobs]',
          'myswimmingclub.theme',
          'myswimmingclub.content',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      # setup_requires=["PasteScript"],
      # paster_plugins=["ZopeSkel"],
      )
