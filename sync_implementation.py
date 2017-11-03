from __future__ import print_function

import os

import pyshogun.database as pysh_db

# Globals
DEBUG = False
OVERRIDE = False
CL_REMOTE_SHOGUN_DB = '\\\\capturelab1\\raid1\\shogunDB\\2017_cl_shogun_remote_database'

if __name__ == '__main__':
    """
    Main entry point here
    """
    if DEBUG:
        source = 'E:\\dev\\python\\shogun\\databases\\source'
        target = 'E:\\dev\\python\\shogun\\databases\\target'
    else:
        if OVERRIDE:
            # TODO Implement arg values parser
            pass
        else:
            # Initialize
            print('{0}'.format('=' * 56))
            print('Framestore Capturelab1 Shogun Database Auto-Sync Utility')
            print('Author: Gerry Corona (Senior Disco TD)')
            print('{0}'.format('=' * 56))
            print('')

            if os.environ['COMPUTERNAME'] == 'SHOGUN':
                CL_LOCAL_SHOGUN_DB = 'G:\\MocapDBs\\2017_cl_shogun_local_database'
                print('Attempting to sync locally from: \n{source} \nto \n{destination}'.format(source=CL_LOCAL_SHOGUN_DB,
                                                                                                destination=CL_REMOTE_SHOGUN_DB))
            else:
                CL_LOCAL_SHOGUN_DB = '\\\\Shogun\\shogunraid\\MocapDBs\\2017_cl_shogun_local_database'
                print('Attempting to sync remotely from: \n{source} \nto \n{destination}'.format(source=CL_LOCAL_SHOGUN_DB,
                                                                                                 destination=CL_REMOTE_SHOGUN_DB))

            print('')

            source = CL_LOCAL_SHOGUN_DB
            target = CL_REMOTE_SHOGUN_DB

    if os.path.isdir(source) and os.path.isdir(target):
        pysh_db.sync(source, target)
    else:
        print('Invalid source database or target database')
