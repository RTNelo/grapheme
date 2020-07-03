from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='grapheme-py2',
      version='0.6.0-py2-1',
      description=u"grapheme backported to Python 2.7",
      long_description=long_description,
      keywords='',
      author=u"Alvin Lindstam",
      author_email='alvin.lindstam@gmail.com',
      url='https://github.com/alvinlindstam/grapheme',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={
          'test': ['pytest', 'sphinx', 'sphinx-autobuild', 'wheel', 'twine']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
      ],
      )
