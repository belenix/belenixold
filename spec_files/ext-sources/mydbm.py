"""Modified Generic interface to all dbm clones.

Instead of

        import dbm
        d = dbm.open(file, 'w', 0666)

use

        import mydbm
        d = mydbm.open(file, 'w')

This module avoids loading the 'dbm' module since on certain Unixes like
Solaris dbm equates to the legacy Unix dbm which has limitations.
"""

import os

class error(Exception):
    pass

#
# TODO: We should be looking for ['dbhash', 'gdbm', 'dumbdbm']
# But gdbm seems to have an issue on Solaris, so avoid it for now.
#
_names = ['dbhash', 'dumbdbm']
_errors = [error]
_defaultmod = None

for _name in _names:
    try:
        _mod = __import__(_name)
    except ImportError:
        continue
    if not _defaultmod:
        _defaultmod = _mod
    _errors.append(_mod.error)

if not _defaultmod:
    raise ImportError, "no dbm clone found; tried %s" % _names

error = tuple(_errors)

def open(file, flag = 'r', mode = 0666):
    # guess the type of an existing database
    from whichdb import whichdb
    result=whichdb(file)
    if result == "":
        # Check if we have a 0-length file
        statinfo = os.stat(file)
        if statinfo.st_size == 0:
            os.remove(file)
            result = None

    if result is None:
        # db doesn't exist
        if 'c' in flag or 'n' in flag:
            # file doesn't exist and the new
            # flag was used so use default type
            mod = _defaultmod
        else:
            raise error, "need 'c' or 'n' flag to open new db"
    elif result == "":
        # db type cannot be determined
        raise error, "db type could not be determined: %s" % file
    else:
        mod = __import__(result)
    return mod.open(file, flag, mode)
