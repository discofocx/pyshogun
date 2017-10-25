from __future__ import print_function

import os
import filecmp
import shutil

DEBUG = True


def compare_directories(source_dir, target_dir):
    """
    Compare the target directory against the source directory,
    if new files are found in the target directory, update the
    target directory
    :param source_dir:
    :param target_dir:
    :return:
    """
    ignore = [os.path.basename(source_dir) + '.enf', os.path.basename(target_dir) + '.enf', 'RCS', 'CVS', 'tags']

    comparison = filecmp.dircmp(source_dir, target_dir, ignore=ignore)

    print(comparison.report_full_closure())
    print(comparison.left_list)
    print(comparison.right_list)
    print(comparison.left_only)

    for subdir in comparison.left_only:
        os.mkdir(os.path.join(target_dir, subdir))
    print('Created {0} new dirs'.format(len(comparison.left_only)))


def sync(source_database, target_database):
    """
    Entry function.
    Attempt to synchronize the provided directories by comparing the target against the source,
    if any new sub dirs or files are present in the source, apply the changes (copy/create - files) on the target.
    :param source_database: string - full path to the source
    :param target_database: string - full path to the target
    :return: boolean - True if the operation was successful
    """
    # compare_directories(source_database, target_database)

    # Files or patterns to ignore
    ignore = [os.path.basename(source_database) + '.enf',
              os.path.basename(target_database) + '.enf',
              'RCS', 'CVS', 'tags']

    # Create a new comparison object
    comparison = filecmp.dircmp(source_database, target_database, ignore=ignore)

    # Show a report
    print(comparison.report_full_closure())
    print('Left Only', comparison.left_only)

    # Attempt to sync
    # Sync any new sub dirs at project level
    if len(comparison.left_only) != 0:
        for project_dir in comparison.left_only:
            os.mkdir(os.path.join(target_database, project_dir))
        print('Created {0} new sub dirs at project level'.format(len(comparison.left_only)))
    else:
        print('Databases are synced at project level')

    # Sync any new sub dirs and files at shoot day level
    if len(comparison.subdirs) != 0:
        for project_dir, obj in comparison.subdirs.iteritems():
            for shoot_dir in obj.left_only:
                if os.path.isdir(os.path.join(source_database, project_dir, shoot_dir)):
                    os.mkdir(os.path.join(target_database, project_dir, shoot_dir))
                else:
                    shutil.copy(os.path.join(source_database, project_dir, shoot_dir), os.path.join(target_database, project_dir))
        print('Created {0} new sub dirs at shoot day level'.format(len(comparison.subdirs)))
    else:
        print('Databases are synced at shoot day level')
