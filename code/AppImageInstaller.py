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
import PySimpleGUI as sg
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
    if not path_to_icon is None:
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
            desktop_file.write(f'Categories={categories}\n')
        if not keywords is None:
            desktop_file.write(f'Keywords={keywords}\n')
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


# gui
def gui():
    global DESKTOP_FILES_DIRECTORY
    global PACKAGES_DIRECTORY
    global _LOGGER

    sg.theme('DarkAmber')

    layout_row_settings = [
        [
            sg.Text('Installation settings', font=('Helvetica', 22))
        ],

        [
            sg.Text('Packages directory', size=(20, 1)),
            sg.InputText(PACKAGES_DIRECTORY.absolute(), key='-PACKAGES_DIRECTORY-'),
            sg.FolderBrowse()
        ],
        [
            sg.Text('.desktop directory', size=(20, 1)),
            sg.InputText(DESKTOP_FILES_DIRECTORY.absolute(), key='-DESKTOP_FILES_DIRECTORY-'),
            sg.FolderBrowse()
        ]
    ]

    layout_row_main = [
        [
            sg.Text('Naming', font=('Helvetica', 22))
        ],

        [
            sg.Text('Package name', size=(20, 1)),
            sg.InputText(key='-PACKAGE_NAME-')
        ],
        [
            sg.Text('Package identifier', size=(20, 1)),
            sg.InputText(key='-PACKAGE_ID-')
        ],
        [
            sg.Text('Generic name', size=(20, 1)),
            sg.InputText(key='-GENERIC_NAME-')
        ],
        [
            sg.Text('Comment', size=(20, 1)),
            sg.InputText(key='-COMMENT-')
        ]
    ]

    layout_row_files = [
        [
            sg.Text('File selection', font=('Helvetica', 22))
        ],

        [
            sg.Text('AppImage', size=(20, 1)),
            sg.InputText(key='-FILE_APPIMAGE-'),
            sg.FileBrowse(file_types=[('AppImage', '*.AppImage')], initial_folder=Path('~/Downloads'))
        ],
        [
            sg.Text('Icon', size=(20, 1)),
            sg.InputText(key='-FILE_ICON-'),
            sg.FileBrowse(file_types=[('JPEG', '*.jpg'), ('PNG', '*.png')], initial_folder=Path('~/Downloads'))
        ],
    ]

    layout_row_metadata_search = [
        [
            sg.Text('Search metadata', font=('Helvetica', 22))
        ],

        [
            sg.Text('Keywords', size=(20, 1)),
            sg.InputText(key='-KEYWORDS-'),
            sg.Text('(";" separated)')
        ],
        [
            sg.Text('Categories', size=(20, 1)),
            sg.InputText(key='-CATEGORIES-'),
            sg.Text('(";" separated)')
        ]
    ]

    layout_row_metadata_execution = [
        [
            sg.Text('Execution metadata', font=('Helvetica', 22))
        ],

        [
            sg.Text('Terminal', size=(20, 1)),
            sg.Drop(values=('False', 'True'), key='-TERMINAL-', auto_size_text=True)
        ]
    ]

    layout = [
        [layout_row_settings],
        [sg.HSeparator(pad=(10, 25))],
        [layout_row_main],
        [sg.HSeparator(pad=(10, 25))],
        [layout_row_metadata_search],
        [sg.HSeparator(pad=(10, 25))],
        [layout_row_files],
        [sg.HSeparator(pad=(10, 25))],
        [layout_row_metadata_execution],
        [sg.HSeparator(pad=(10, 25))],
        [sg.Button('Install')]
    ]

    window = sg.Window('AppImageInstaller', layout)

    while True:
        event, values = window.read()
        if event == 'Install':
            # Get values from input fields
            tmp_packages_directory = values['-PACKAGES_DIRECTORY-']
            tmp_desktop_files_directory = values['-DESKTOP_FILES_DIRECTORY-']

            package_id = values['-PACKAGE_ID-']
            package_name = values['-PACKAGE_NAME-']
            generic_name = values['-GENERIC_NAME-']

            file_appimage = Path(values['-FILE_APPIMAGE-'])
            file_icon = Path(values['-FILE_ICON-'])
            
            comment = values['-COMMENT-']
            categories = values['-CATEGORIES-']
            keywords = values['-KEYWORDS-']
            terminal = values['-TERMINAL-']

            # Sanitize values
            if tmp_packages_directory == '' or not Path(tmp_packages_directory).exists():
                tmp_packages_directory = None
            if tmp_desktop_files_directory == '' or not Path(tmp_desktop_files_directory).exists():
                tmp_desktop_files_directory = None

            if package_id == '':
                package_id = None
            if package_name == '':
                package_name = None
            if generic_name == '':
                generic_name = None
            if not (file_appimage.exists() and file_appimage.is_file()):
                file_appimage = None
            if not (file_icon.exists() and file_icon.is_file()):
                file_icon = None
            if comment == '':
                comment = None
            if categories == '':
                categories = None
            if keywords == '':
                keywords = None
            if terminal == '':
                terminal = None
            
            # Check if all required values were supplied
            settings_directorys_invalid = []
            if tmp_packages_directory is None:
                settings_directorys_invalid.append('packages_directory')
            if tmp_desktop_files_directory is None:
                settings_directorys_invalid.append('desktop_files_directory')

            if len(settings_directorys_invalid) > 0:
                _LOGGER.warn(f'Can not install package. Directory does not exist: {", ".join(settings_directorys_invalid)}')
                sg.popup('Can not install package.', f'Directory does not exist: {", ".join(settings_directorys_invalid)}')

            missing_arguments = []
            if package_id is None:
                missing_arguments.append('package_id')
            if package_name is None:
                missing_arguments.append('package_name')
            if file_appimage is None:
                missing_arguments.append('file_appimage')

            if len(missing_arguments) > 0:
                _LOGGER.warn(f'Can not install package. Arguments missing: {", ".join(missing_arguments)}')
                sg.popup('Can not install package.', f'Arguments missing: {", ".join(missing_arguments)}')
                continue

            install_package(package_id = package_id,
                            package_name = package_name,
                            path_to_appimage = file_appimage,
                            path_to_icon = file_icon,
                            comment = comment,
                            categories = categories,
                            keywords = keywords,
                            terminal = terminal,
                            genericName = generic_name)
        elif event == sg.WIN_CLOSED:
            break


gui()
#install_package('test_package', 'Test Package', Path('./Test.AppImage'), Path('./Test.png'), 'Ein Kommentar', ['Audio', 'Video'], ['find', 'me'], False, 'Test')