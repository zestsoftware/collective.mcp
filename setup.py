from setuptools import setup, find_packages
import os


def get_file_contents(filename):
    file_path = os.path.join(filename)
    this_file = open(file_path)
    contents = this_file.read().strip()
    this_file.close()
    return contents

history = get_file_contents('CHANGES.rst')
readme = get_file_contents('README.rst')
long = "%s\n\n\n%s" % (readme, history)

setup(name='collective.mcp',
      version='0.5.dev0',
      description="Macish Control Panel for Plone.",
      long_description=long,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          ],
      keywords='mac control panel',
      author='Zest Software',
      author_email='info@zestsoftware.nl',
      url='https://github.com/zestsoftware/collective.mcp',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.multimodeview'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
