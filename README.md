# AppImageInstaller - The installer for non-installable programs.

# Install AppImages and other non-installable programs and create XDG Desktop Menu entries.

**NOTE: This project is only relevant for Linux-Users.**

AppImages are great because they are easy to use and work on nearly every Linux
system. The only downside is that you can not install them and they don't appear
in the Desktop Menu. The same downside exists for e.g. Bash- and Python scripts.

With AppImageInstaller you can easily organize all your AppImages and other
non-installable programs in a central location and create a .desktop file
containing all relevant information about the program.

## Install AppImageInstaller

Installing is not required, however I recommend it to make using it easier.
After installing you should find AppImageInstaller in your Desktop Menu.

We will use AppImageInstaller to install itself. But first we have to clone the
repository.

```
git clone git@github.com:Andreas-Menzel/AppImageInstaller.git

cd ./code/

python3 AppImageInstaller.py --ui none --app_id 'appimageinstaller' --app_name 'AppImageInstaller' --path_executable './AppImageInstaller.py' --paths_add_files 'logHandler.py' --comment 'Have a look at https://github.com/Andreas-Menzel/AppImageInstaller.' --keywords 'app' 'application' 'image' 'appimage' 'installer' --generic_name 'Installer'
```

AppImageInstaller is now located at '~/AppImages/'.

## How can I use AppImageInstaller?

You can use one of three user interfaces. Passing `--ui <ui>` to
AppImageInstaller will select the user interface.

1) **GUI - graphical user interface**

    This is the standard when executing AppImageInstaller.

2) **TUI - terminal user interface**

    You can use this ui when AppImageInstaller is executed on a system without
    a desktop environment or if you are accessing it via SSH.

3) **none - no user interface**

    Use this to install an application with a single command non-interactively.

I recommend using the graphical user interface, but if you really love using
the terminal and don't want to see the beautiful gui, you can absolutely access
every feature via the terminal alone (either TUI or none).

### none - Non-interactive command line-execution

If you want to use this mode of execution, you have to pass all arguments to
AppImageInstaller directly. See `--help` or the
[Parameters](#Parameters)-section for more details.

Example:

```
python3 AppImageInstaller.py --ui 'none' --app_id 'test_app' --app_name 'Test App' --path_executable '/home/user/Downloads/App.AppImage'
```

### GUI - Interactive graphical user interface

You can pass arguments when executing AppImageInstaller to pre-select some of
the values. See `--help` or the [Parameters](#Parameters)-section for more
details.

Example:

```
python3 AppImageInstaller.py --ui 'gui'
```

or

```
python3 AppImageInstaller.py
```

### TUI - Interactive terminal user interface

You can pass arguments when executing AppImageInstaller to pre-select some of
the values. See `--help` or the [Parameters](#Parameters)-section for more
details.

Example:

```
python3 AppImageInstaller.py --ui 'tui'
```

### Parameters

```
usage: AppImageInstaller [-h] [--version] [--ui {gui,tui,none}] [--app_id APP_ID] [--app_name APP_NAME] [--path_executable PATH_EXECUTABLE]
                         [--paths_add_files PATHS_ADD_FILES [PATHS_ADD_FILES ...]] [--path_add_files_dir PATH_ADD_FILES_DIR [PATH_ADD_FILES_DIR ...]] [--path_icon PATH_ICON]
                         [--comment COMMENT] [--categories CATEGORIES [CATEGORIES ...]] [--keywords KEYWORDS [KEYWORDS ...]] [--terminal TERMINAL] [--generic_name GENERIC_NAME]

Install AppImages and other non-installable programs and create XDG Desktop Menu entries.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --ui {gui,tui,none}   Specify the user interface. Select between graphical user interface, terminal user interface or non-interactive.
  --app_id APP_ID       ID of the app. Can be same as app_name
  --app_name APP_NAME   Name of the app.
  --path_executable PATH_EXECUTABLE
                        Path to the (main) executable file.
  --paths_add_files PATHS_ADD_FILES [PATHS_ADD_FILES ...]
                        Paths to additional app files. The files will be copied to the same directory as the main executable.
  --path_add_files_dir PATH_ADD_FILES_DIR [PATH_ADD_FILES_DIR ...]
                        Path to a directory containing additional app files. The files will be copied to the same directory as the main executable.
  --path_icon PATH_ICON
                        Path to the app icon image.
  --comment COMMENT     Comment describing the app.
  --categories CATEGORIES [CATEGORIES ...]
                        Categories.
  --keywords KEYWORDS [KEYWORDS ...]
                        Keywords.
  --terminal TERMINAL   .desktop parameter: Terminal
  --generic_name GENERIC_NAME
                        Generic name of the app.
```
