from setuptools import setup

setup(name='mogilefs_storage',
      version='0.1a',
      packages=['mogilefs_storage'],
      description='MogileFS FileStorage for Django',
      author='Daniel E. Bruce',
      author_email='ircubic@gmail.com',
      zip_safe=True,
# Commented out, pending fix for https://bugs.launchpad.net/zc.buildout/+bug/285121
#      install_requires = ['mogilefs'],
#      dependency_links = [
#          'http://www.albany.edu/~ja6447/mogilefs.py#egg=mogilefs-0.1'
#      ],
)
