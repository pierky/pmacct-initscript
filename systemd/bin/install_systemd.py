#!/usr/bin/env python3
"""Script to install pmacct daemon files in the correct location.

Logic:

    - Verify whether the script is being run by root or sudo user
    - Check to see whether this is a systemd system
    - Check existence of /etc/systemd/system/multi-user.target directory
    - Check symlink location of files in that directory
    - Copy files to that symlink location
    - Reload the systemd daemon

"""

import sys
import os
from subprocess import check_output, call
from shutil import copyfile


def log(msg):
    """Log messages to STDIO and exit.

    Args:
        msg: String to print

    Returns:
        None

    """
    # Die!
    message = 'ERROR: {}'.format(msg)
    print(message)
    sys.exit(0)


def _filepaths(directory, full_paths=True):
    """Get the filenames in the directory.

    Args:
        directory: Directory with the files
        full_paths: Give full paths if True

    Returns:
        result: List of filenames

    """
    # Initialize key variables
    if bool(full_paths) is True:
        result = [
            os.path.join(directory, filename) for filename in os.listdir(
                directory) if os.path.isfile(
                    os.path.join(directory, filename))]
    else:
        result = [filename for filename in os.listdir(
            directory) if os.path.isfile(os.path.join(directory, filename))]

    return result


def _copy_service_files(target_directory):
    """Copy service files to target directory.

    Args:
        target_directory: Target directory

    Returns:
        None

    """
    # Initialize key variables
    src_dst = {}

    # Determine the directory with the service files
    exectuable_directory = os.path.dirname(os.path.realpath(__file__))
    source_directory = '{}/system'.format(
        os.path.abspath(os.path.join(exectuable_directory, os.pardir)))

    # Get source and destination file paths
    source_filepaths = _filepaths(source_directory)
    for filepath in source_filepaths:
        src_dst[filepath] = '{}/{}'.format(
            target_directory, os.path.basename(filepath))

    # Copy files
    for source_filepath, destination_filepath in sorted(src_dst.items()):
        copyfile(source_filepath, destination_filepath)

    # Make systemd aware of the new services
    activation_command = 'systemctl daemon-reload'
    call(activation_command.split())

    # Print success message
    source_files = _filepaths(source_directory, full_paths=False)
    print('''\
SUCCESS! You are now able to start/stop and enable/disable the following \
systemd services: {}'''.format(', '.join(source_files)))


def _symlink_dir(directory):
    """Get directory in which the symlinked files are located.

    Args:
        directory: Directory with the symlinks

    Returns:
        result: Directory to which the files have symlinks

    """
    # Initialize key variables
    data_dictionary = {}

    # Get all the filenames in the directory
    filenames = _filepaths(directory)

    # Get the name of the directory to which the files are symlinked
    for filename in filenames:
        symlink_target = os.readlink(filename)
        data_dictionary[
            os.path.dirname(os.path.abspath(symlink_target))] = True

    # Get the first directory in the dictionary
    for key in sorted(data_dictionary.keys()):
        result = key
        break
    return result


def main():
    """Run the functions for installation.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    etc_dir = '/etc/systemd/system/multi-user.target.wants'

    # Verify whether the script is being run by root or sudo user
    if bool(os.getuid()) is True:
        log('This script must be run as the "root" user '
            'or with "sudo" privileges')

    # Check to see whether this is a systemd system
    try:
        check_output(['pidof', 'systemd'])
    except:
        log('This is not a "systemd" system. This script should not be run.')

    # Check existence of /etc/systemd/system/multi-user.target directory
    if os.path.isdir(etc_dir) is False:
        log('Expected systemd directory "{}" does not exist.'.format(etc_dir))

    # Check symlink location of files in that directory
    target_directory = _symlink_dir(etc_dir)

    # Copy files
    _copy_service_files(target_directory)


if __name__ == '__main__':
    main()
