A FileStorage implementation for using MogileFS with Django
===

Requirements
---
Requires http://www.albany.edu/~ja6447/mogilefs.py present somewhere
on the python path.

This dependency couldn't be included in the setup.py file, because it
breaks when using buildout.
Refer to https://bugs.launchpad.net/zc.buildout/+bug/285121

Usage
---
To use, add something like this to your settings.py, substituting the values
for MOGILE_TRACKERS and MOGILE_DOMAIN as appropriate:

  MOGILE_TRACKERS='127.0.0.1:7001,testserver:7001'
  MOGILE_DOMAIN='default'
  DEFAULT_FILE_STORAGE='mogilefs_storage.MogileFSStorage'