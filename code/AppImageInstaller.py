#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# AppImageInstaller
#
# Installs a .AppImage by moving it to a predefined location and creating a
#     .desktop file.
#
# https://github.com/Andreas-Menzel/AppImageInstaller
#-------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# @copyright: Copyright (c) 2022 Andreas Menzel
#-------------------------------------------------------------------------------


from pathlib import Path
from shutil import copyfile

import logHandler


_LOGGER = logHandler.getSimpleLogger(__name__, streamLogLevel=logHandler.INFO, fileLogLevel=logHandler.DEBUG)

# Directory where the .AppImages will be installed
#
#PACKAGES_DIRECTORY = Path('~/AppImages')
PACKAGES_DIRECTORY = Path('./packages')

# Directory where the .desktop files are stored.
#
#DESKTOP_FILES_DIRECTORY = Path('~/.local/share/applications')
DESKTOP_FILES_DIRECTORY = Path('./desktop_files')


# install_package
#
# @param    str         package_id          A short identifier of the package.
#                                               Can be same as package_name.
# @param    str         package_name        Name of the package to be installed.
# @param    Path        path_to_appimage    Path to the .AppImage file.
# @param    Path / None path_to_icon        Path to the icon.
# @param    str / None  comment             .desktop entry: Comment.
# @param    [str] / None categories         .desktop entry: Categories.
# @param    [str] / None keywords           .desktop entry: Keywords.
# @param    bool / None terminal            .desktop entry: Terminal.
# @param    str / None  genericName         .desktop entry: GenericName.
#
# @return   int         0   Everything fine. AppImage installed.
# @return   int         1   Package directory already exists. Maybe the package
#                               is already installed?
# @return   int         2   The .desktop directory does not exist.
# @return   int         3   AppImage not found.
# @return   int         4   Icon not found.
def install_package(package_id: str, package_name: str, path_to_appimage: Path,
                    path_to_icon: Path, comment: str = None,
                    categories: [str] = None, keywords: [str] = None,
                    terminal: bool = False, genericName: str = None) -> int:
    global _LOGGER
    global DESKTOP_FILES_DIRECTORY
    global PACKAGES_DIRECTORY

    package_path = PACKAGES_DIRECTORY.joinpath(package_id)

    # Check if package is already installed
    if package_path.exists():
        _LOGGER.error('Package directory already exists. Maybe the package is already installed?')
        return 1
    package_path.mkdir(parents=True, exist_ok=False)
    
    # Check if .desktop directory exists
    desktop_file_path = DESKTOP_FILES_DIRECTORY.joinpath(f'{package_id}.desktop')
    if not DESKTOP_FILES_DIRECTORY.exists():
        _LOGGER.error(f'The .desktop directory does not exist! ({DESKTOP_FILES_DIRECTORY})')
        return 2

    package_path_appimage = package_path.joinpath(f'{package_id}.AppImage')
    package_path_icon = package_path.joinpath(f'{package_id}{path_to_icon.suffix}')

    # Create .desktop file
    with open(desktop_file_path, 'w') as desktop_file:
        desktop_file.write('[Desktop Entry]\n\n')
        desktop_file.write('Type=Application\n')
        desktop_file.write(f'Name={package_name}\n')
        if not genericName is None:
            desktop_file.write(f'GenericName={genericName}\n')
        # TODO: In Anführungszeichen ("")?
        desktop_file.write(f'Exec={package_path_appimage.absolute()}\n')
        if not path_to_icon is None:
            # TODO: In Anführungszeichen ("")?
            desktop_file.write(f'Icon={package_path_icon.absolute()}\n')
        if not comment is None:
            desktop_file.write(f'Comment={comment}\n')
        if not categories is None:
            # TODO: ';' auch am Ende?
            desktop_file.write(f'Categories={";".join(categories)}\n')
        if not keywords is None:
            # TODO: ';' auch am Ende?
            desktop_file.write(f'Keywords={";".join(keywords)}\n')
        if not terminal is None:
            desktop_file.write(f'Terminal={terminal}\n')

    # Copy .AppImage file
    if not path_to_appimage.exists():
        _LOGGER.error(f'AppImage not found! ({path_to_appimage})')
        return 3
    copyfile(path_to_appimage, package_path_appimage)

    # Copy icon
    if not path_to_icon is None:
        if not path_to_icon.exists():
            _LOGGER.error(f'Icon not found! ({path_to_icon})')
            return 4
        copyfile(path_to_icon, package_path_icon)
    
    _LOGGER.info('AppImage installed successfully.')
    return 0


install_package('test_package', 'Test Package', Path('./Test.AppImage'), Path('./Test.png'), 'Ein Kommentar', ['Audio', 'Video'], ['find', 'me'], False, 'Test')