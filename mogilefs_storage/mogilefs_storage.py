import os
import mimetypes

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.text import force_unicode
from django.core.files.storage import Storage

__all__ = ['MogileFSStorage', 'MogileFileWrapper']

try:
    import mogilefs
except ImportError:
    raise ImproperlyConfigured, "Could not load mogilefs dependency.\
    \nSee http://mogilefs.pbworks.com/Client-Libraries"

class MogileFSStorage(Storage):
    """MogileFS filesystem storage"""
    def __init__(self):
        for setting in ('MOGILE_TRACKERS', 'MOGILE_DOMAIN'):
            if not hasattr(settings, setting):
                raise ImproperlyConfigured('The setting %s must be set to ' +
                                           'use MogileFSStorage' % setting)
        self.trackers = settings.MOGILE_TRACKERS.split(',')
        self.domain = settings.MOGILE_DOMAIN
        self.client = mogilefs.Client(domain=self.domain, trackers=self.trackers)
    
    def filesize(self, filename):
        raise NotImplemented
    
    def path(self, filename):
        raise NotImplemented
    
    def url(self, filename):
        raise NotImplemented
    
    def _open(self, filename, mode='rb'):
        return MogileFileWrapper(filename, self, mode)

    def _read(self, filename):
        return self.client[filename]
                                 
    def exists(self, filename):
        return filename in self.client
    
    def _save(self, filename, contents):
        success = self.client.send_file(filename, contents)
        if not success:
            raise IOException("Unable to save file: %s" % filename)
        return force_unicode(filename)
    
    def delete(self, filename): 
        self.client.delete(filename)

class MogileFileWrapper(File):
    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self._size = None
        self.file = StringIO()
    
    @property
    def size(self):
        if self._size is None:
            self._read_in()
        return self._size

    def _read_in(self):
        data = self._storage._read(self._name)
        self.file = StringIO(data)
        self._size = len(data)

    def read(self, num_bytes=None):
        if not self._is_dirty:
            self._read_in()
        return self.file.getvalue()
    
    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was not opened with write access.")
        self.file = StringIO(content)
        self._is_dirty = True
        
    def close(self):
        if self._is_dirty:
            self._storage._save(self._name, self.file)
        self.file.close()

def get_random_string(amount=8):
    import string
    import random
    alphabet = string.letters+string.digits
    return "".join([random.choice(alphabet)
                    for i in xrange(amount)])
                    

def test(trackers, domain):
    settings.MOGILE_TRACKERS = ','.join(trackers)
    settings.MOGILE_DOMAIN = domain
    c = mogilefs.Client(domain=domain, trackers=trackers)
    storage = MogileFSStorage()

    def get_test_name():
        return 'MFSS' + get_random_string(8)

    test_name = get_test_name()
    test_data = get_random_string(1024*10)
    
    f = storage.open(test_name, 'w')
    f.write(test_data)
    f.close()
    assert test_data == c[test_name]

    test_name = get_test_name()
    test_data = get_random_string(1024*10)

    c[test_name] = test_data
    f = storage.open(test_name)
    read_text = f.read()
    f.close()
    assert test_data == read_text

    print "Great success!"
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        raise Exception("Not enough arguments")
    trackers = [x.strip() for x  in sys.argv[1].split(',')]
    domain = sys.argv[2]
    try:
        test(trackers, domain)
    except AssertionError, e:
        print "Test Failed: %s" % e
