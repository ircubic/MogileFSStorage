A FileStorage implementation for using MogileFS with Django

Requires http://www.albany.edu/~ja6447/mogilefs.py present somewhere
on the python path.

This dependency couldn't be included in the setup.py file, because it
breaks when using buildout.
Refer to https://bugs.launchpad.net/zc.buildout/+bug/285121
