from __future__ import print_function

import os
import sys
import filecmp
import shutil
import time

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


def _sync_project_level(comparison_obj):
    """
    Generate lists of new directories and new files at Project level
    :type comparison_obj: file.cmp.dircmp object
    :param comparison_obj: The comparison on where we operate
    :return: set - (List of new folders, List of new files)
    """
    new_files = list()
    new_dirs = list()

    if len(comparison_obj.left_only) != 0:
        for project_dir in comparison_obj.left_only:
            if os.path.isdir(os.path.join(comparison_obj.left, project_dir)):
                new_dirs.append(os.path.join(comparison_obj.right, project_dir))
                # os.mkdir(os.path.join(comparison_obj.right, project_dir))
                # new_dirs += 1
            else:
                new_files.append((os.path.join(comparison_obj.left, project_dir), os.path.join(comparison_obj.right)))
                # shutil.copy(os.path.join(comparison_obj.left, project_dir),
                #             os.path.join(comparison_obj.right, project_dir))
                # new_files += 1

    return new_dirs, new_files


def _sync_shoot_day_level(project_obj):
    """
    Generate lists of new directories and new files at Shoot day level
    :param project_obj:
    :return: set - (List of new folders, List of new files)
    """
    new_files = list()
    new_dirs = list()

    if len(project_obj.subdirs) != 0:
        for project_dir, project_obj in project_obj.subdirs.iteritems():
            for shoot_dir in project_obj.left_only:
                if os.path.isdir(os.path.join(project_obj.left, shoot_dir)):
                    new_dirs.append(os.path.join(project_obj.right, shoot_dir))
                    # os.mkdir(os.path.join(project_obj.right, shoot_dir))
                    # new_dirs += 1
                else:
                    new_files.append((os.path.join(project_obj.left, shoot_dir), os.path.join(project_obj.right)))
                    # shutil.copy(os.path.join(project_obj.left, shoot_dir), project_obj.right)
                    # new_files += 1

    return new_dirs, new_files


def _sync_session_level(shoot_day_obj):
    """
    Generate lists of new directories and new files at Session level
    :param shoot_day_obj:
    :return: set - (List of new folders, List of new files)
    """
    new_files = list()
    new_dirs = list()

    for project_dir, project_obj in shoot_day_obj.subdirs.iteritems():
        if len(project_obj.subdirs) != 0:
            for shoot_day_dir, shoot_day_obj in project_obj.subdirs.iteritems():
                for session_dir in shoot_day_obj.left_only:
                    if os.path.isdir(os.path.join(shoot_day_obj.left, session_dir)):
                        new_dirs.append(os.path.join(shoot_day_obj.right, session_dir))
                        # os.mkdir(os.path.join(shoot_day_obj.right, session_dir))
                        # new_dirs += 1
                    else:
                        new_files.append(
                            (os.path.join(shoot_day_obj.left, session_dir), os.path.join(shoot_day_obj.right)))
                        # shutil.copy(os.path.join(shoot_day_obj.left, session_dir), shoot_day_obj.right)
                        # new_files += 1

    return new_dirs, new_files


def _sync_takes_level(takes_obj):
    """
    Generate lists of new directories and new files at Takes level
    :param takes_obj:
    :return: set - (List of new folders, List of new files)
    """
    new_files = list()
    new_dirs = list()

    for project_dir, project_obj in takes_obj.subdirs.iteritems():
        for shoot_day_dir, shoot_day_obj in project_obj.subdirs.iteritems():
            if len(shoot_day_obj.subdirs) != 0:
                for session_dir, session_obj in shoot_day_obj.subdirs.iteritems():
                    for take in session_obj.left_only:
                        if os.path.isdir(os.path.join(session_obj.left, take)):
                            new_dirs.append(os.path.join(session_obj.right, take))
                            # os.mkdir(os.path.join(session_obj.right, take))
                            # new_dirs += 1
                        else:
                            new_files.append((os.path.join(session_obj.left, take), os.path.join(session_obj.right)))
                            # shutil.copy(os.path.join(session_obj.left, take), session_obj.right)
                            # new_files += 1
    return new_dirs, new_files


def _process_sync(tree_index, tree, dirs, files):
    """
    Run the make dir and copy files actions salvaged from the sync operations
    :param tree_index:
    :param dirs:
    :param files:
    :return:
    """

    if len(dirs) == 0 and len(files) == 0:
        print('Databases at ({level}) level are synced'.format(level=tree[tree_index]))
    else:
        for index, l_dir in enumerate(dirs):
            os.mkdir(l_dir)
            progress = ((index + 1) * 100) / len(dirs)
            sys.stdout.write('\rDirectory Sync Progress at ({level}) level {progress}% - '.format(level=tree[tree_index],
                                                                                               progress=progress))
            # sys.stdout.flush()
            if DEBUG:
                time.sleep(0.2)
        print('Created ({dirs}) new directories at ({level})'.format(dirs=len(dirs), level=tree[tree_index]))

        for index, l_file in enumerate(files):
            source_file, destination_file = l_file
            shutil.copy(source_file, destination_file)
            progress = ((index + 1) * 100) / len(files)
            sys.stdout.write('\rFile Sync Progress at ({level}) level {progress}% - '.format(level=tree[tree_index],
                                                                                          progress=progress))
            # sys.stdout.flush()
            if DEBUG:
                time.sleep(0.2)
        print('Created ({files}) new files at ({level})'.format(files=len(files), level=tree[tree_index]))


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

    database_tree = {0: 'Project',
                     1: 'Shoot Day',
                     2: 'Session',
                     3: 'Takes'}

    # Attempt to sync
    for index, level in database_tree.iteritems():
        if index == 0:
            project_comp = filecmp.dircmp(source_database, target_database, ignore=ignore)
            dirs, files = _sync_project_level(project_comp)
            _process_sync(index, database_tree, dirs, files)
        elif index == 1:
            shoot_day_comp = filecmp.dircmp(source_database, target_database, ignore=ignore)
            dirs, files = _sync_shoot_day_level(shoot_day_comp)
            _process_sync(index, database_tree, dirs, files)
        elif index == 2:
            session_comp = filecmp.dircmp(source_database, target_database, ignore=ignore)
            dirs, files = _sync_session_level(session_comp)
            _process_sync(index, database_tree, dirs, files)
        elif index == 3:
            take_comp = filecmp.dircmp(source_database, target_database, ignore=ignore)
            dirs, files = _sync_takes_level(take_comp)
            _process_sync(index, database_tree, dirs, files)
