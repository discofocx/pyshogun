from __future__ import print_function

import pyshogun.database as pysh_db

DEBUG = True

if __name__ == '__main__':
    if DEBUG:
        source = 'E:\\dev\\python\\shogun\\databases\\source'
        target = 'E:\\dev\\python\\shogun\\databases\\target'
    else:
        # Get database paths from the application or user
        pass

    pysh_db.sync(source, target)
