from setuptools import setup, find_packages
import os

def get_file_contents(filename):
    file_path = os.path.join(filename)
    this_file = open(file_path)
    contents = this_file.read().strip()
    this_file.close()
    return contents

version = get_file_contents('collective/mcp/version.txt')
history = get_file_contents('collective/mcp/HISTORY.rst')
roadmap = get_file_contents('collective/mcp/ROADMAP.rst')
readme = get_file_contents('README.rst')
long = "%s\n\n\n%s\n\n%s" % (readme, roadmap, history)

setup(name='collective.mcp',
      version=version,
      description="Macish Control Panel for Plone.",
      long_description=long,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
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
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
