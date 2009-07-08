from setuptools import setup

long_description = open("README.txt").read()

setup(name='mogilefs_storage',
      version='0.1b',
      packages=['mogilefs_storage'],
      description='MogileFS FileStorage for Django',
      long_description=long_description,
      license='MIT',
      author='Daniel E. Bruce',
      author_email='ircubic@gmail.com',
      zip_safe=True,
# Commented out, pending fix for https://bugs.launchpad.net/zc.buildout/+bug/285121
#      install_requires = ['mogilefs'],
#      dependency_links = [
#          'http://www.albany.edu/~ja6447/mogilefs.py#egg=mogilefs-0.1'
#      ],
)
