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
from shutil import copyfile, copytree
import stat

import logHandler


_LOGGER = logHandler.getSimpleLogger(__name__, streamLogLevel=logHandler.INFO, fileLogLevel=logHandler.DEBUG)

# Directory where the .AppImages will be installed
PACKAGES_DIRECTORY = Path.home().joinpath('AppImages')

# Directory where the .desktop files are stored.
DESKTOP_FILES_DIRECTORY = Path.home().joinpath('.local/share/applications')


# install_package
#
# @param    str             app_id              A short identifier of the app
#                                                   Can be same as app_name.
# @param    str             app_name            Name of the app to be installed.
# @param    Path            path_executable     Path to the executable.
# @param    [Path] / None   paths_add_files     Paths to additional app files.
# @param    Path / None     path_add_files_dir  Path to directory containing
#                                                   additional app files.
# @param    Path / None     path_icon           Path to the icon.
# @param    str / None      comment             .desktop entry: Comment.
# @param    [str] / None    categories          .desktop entry: Categories.
# @param    [str] / None    keywords            .desktop entry: Keywords.
# @param    bool / None     terminal            .desktop entry: Terminal.
# @param    str / None      genericName         .desktop entry: GenericName.
#
# @return   int         0   Everything fine. App installed.
# @return   int         1   App directory already exists. Maybe the app is
#                               already installed?
# @return   int         2   The .desktop directory does not exist.
# @return   int         3   Executable not found.
# @return   int         4   Additional app files not found.
# @return   int         5   Icon not found.
def install_package(app_id: str, app_name: str, path_executable: Path,
                    paths_add_files: [Path], path_add_files_dir: Path,
                    path_icon: Path, comment: str = None,
                    categories: [str] = None, keywords: [str] = None,
                    terminal: bool = False, genericName: str = None) -> int:
    global _LOGGER
    global DESKTOP_FILES_DIRECTORY
    global PACKAGES_DIRECTORY

    app_path = PACKAGES_DIRECTORY.joinpath(app_id)
    app_path_application = app_path.joinpath('application')

    # Check if app is already installed
    if app_path.exists():
        _LOGGER.error('App directory already exists. Maybe the app is already installed?')
        return 1
    app_path_application.mkdir(parents=True)
    
    # Check if .desktop-files directory exists
    desktop_file_path = DESKTOP_FILES_DIRECTORY.joinpath(f'{app_id}.desktop')
    app_desktop_file_path = app_path.joinpath(f'{app_id}.desktop')
    if not DESKTOP_FILES_DIRECTORY.exists():
        _LOGGER.error(f'The .desktop-files directory does not exist! ({DESKTOP_FILES_DIRECTORY})')
        return 2

    # Set executable- and icon-path of app
    app_path_executable = app_path_application.joinpath(path_executable.name)
    if not path_icon is None:
        app_path_icon = app_path.joinpath(path_icon.name)

    # Create .desktop file
    with open(app_desktop_file_path, 'w') as desktop_file:
        desktop_file.write('[Desktop Entry]\n\n')
        desktop_file.write('Type=Application\n')
        desktop_file.write(f'Name={app_name}\n')
        if not genericName is None:
            desktop_file.write(f'GenericName={genericName}\n')
        # TODO: In Anführungszeichen ("")?
        desktop_file.write(f'Exec={app_path_executable.absolute()}\n')
        if not path_icon is None:
            # TODO: In Anführungszeichen ("")?
            desktop_file.write(f'Icon={app_path_icon.absolute()}\n')
        if not comment is None:
            desktop_file.write(f'Comment={comment}\n')
        if not categories is None:
            desktop_file.write(f'Categories={categories}\n')
        if not keywords is None:
            desktop_file.write(f'Keywords={keywords}\n')
        if not terminal is None:
            desktop_file.write(f'Terminal={terminal}\n')
    copyfile(app_desktop_file_path, desktop_file_path)

    # Copy executable file and make executable
    if not path_executable.exists():
        _LOGGER.error(f'Executable not found! ({path_executable})')
        return 3
    copyfile(path_executable, app_path_executable)
    app_path_executable.chmod(app_path_executable.stat().st_mode | stat.S_IEXEC)

    # Copy additional app files
    if not paths_add_files is None:
        files_not_found = []
        for path in paths_add_files:
            if not path.exists():
                files_not_found.append(path)
            copyfile(path, app_path_application.joinpath(path.name))
        if len(files_not_found) > 0:
            _LOGGER.error(f'Additional app file(s) not found! ({";".join(files_not_found)})')
            return 4
    
    if not path_add_files_dir is None:
        if not path_add_files_dir.exists():
            _LOGGER.error(f'Additional app files directory not found! ({path_add_files_dir})')
            return 4
        copytree(path_add_files_dir, app_path_application, dirs_exist_ok=True)

    # Copy icon
    if not path_icon is None:
        if not path_icon.exists():
            _LOGGER.error(f'Icon not found! ({path_icon})')
            return 5
        copyfile(path_icon, app_path_icon)
    
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
            sg.FolderBrowse(initial_folder=PACKAGES_DIRECTORY)
        ],
        [
            sg.Text('.desktop directory', size=(20, 1)),
            sg.InputText(DESKTOP_FILES_DIRECTORY.absolute(), key='-DESKTOP_FILES_DIRECTORY-'),
            sg.FolderBrowse(initial_folder=DESKTOP_FILES_DIRECTORY)
        ]
    ]

    layout_row_main = [
        [
            sg.Text('Naming', font=('Helvetica', 22))
        ],

        [
            sg.Text('Package name', size=(20, 1)),
            sg.InputText(key='-APP_NAME-')
        ],
        [
            sg.Text('Package identifier', size=(20, 1)),
            sg.InputText(key='-APP_ID-')
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

            app_id = values['-APP_ID-']
            app_name = values['-APP_NAME-']
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

            if app_id == '':
                app_id = None
            if app_name == '':
                app_name = None
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
            if app_id is None:
                missing_arguments.append('app_id')
            if app_name is None:
                missing_arguments.append('app_name')
            if file_appimage is None:
                missing_arguments.append('file_appimage')

            if len(missing_arguments) > 0:
                _LOGGER.warn(f'Can not install package. Arguments missing: {", ".join(missing_arguments)}')
                sg.popup('Can not install package.', f'Arguments missing: {", ".join(missing_arguments)}')
                continue

            install_package(app_id = app_id,
                            app_name = app_name,
                            path_executable = file_appimage,
                            path_icon = file_icon,
                            comment = comment,
                            categories = categories,
                            keywords = keywords,
                            terminal = terminal,
                            genericName = generic_name)

            sg.popup('Installation succesful!')
            break
        elif event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    #gui()
    install_package('test2', 'Test 2', Path('/home/andreas/Documents/PrusaSlicer-2.4.2+linux-x64-GTK3-202204251120.AppImage'), [Path('/home/andreas/Documents/file1'), Path('/home/andreas/Documents/file2')], Path('/home/andreas/Documents/app_files'), Path('/home/andreas/Documents/Screenshot from 2022-07-04 08-37-14.png'))