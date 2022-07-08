# AppImageInstaller - The installer for non-installable programs.

# Install AppImages and other non-installable programs and create XDG Desktop Menu entries.

**NOTE: This project is only relevant for Linux-Users.**

AppImages are great because they are easy to use work on nearly every Linux
system. The only downside is that you can not install them and they don't appear
in the Desktop Menu. The same downside exists for e.g. Bash- and Python scripts.

With AppImageInstaller you can easily organize all your AppImages and other
non-installable programs in a central location and create a .desktop file
containing all relevant information about the program.

AppImageInstaller also comes with functions to reinstall multiple programs
(can be useful if you want to move programs to another / new system). Installing
and de-installing a program is as simple as clicking a button.

## Install AppImageInstaller

Installing is not required, however I recommend it to make using it easier
(especially if you want to change one of the directories). After installing you
should find AppImageInstaller in your Desktop Menu.

Execute `code/AppImageInstaller_install.py`.

```
python3 AppImageInstaller_install.py
```

You can also specify the directory where the packages are installed into and
the directory where the .desktop files are saved:

```
python3 AppImageInstaller_install.py --packages_directory <pack_dir> --desktop_files_directory <desk_dir>
```

packages_directory is where the packages will be installed into. The default is
`~/AppImages`.

desktop_files_directory is where the .desktop files will be placed. The default
is `~/.local/share/applications`.

## How can I use AppImageInstaller?

I recommend using the graphical user interface, but if you really love using
the terminal and don't want to see the beautiful gui, you can absolutely access
every feature via the terminal alone.

### Interactive graphical user interface

#### Install a program

TODO

#### Deinstall a program

TODO

#### Create a backup

TODO

#### Reinstall a backup

TODO

### Single-command terminal execution

#### Install a program

TODO

#### Deinstall a program

TODO

#### Create a backup

TODO

#### Reinstall a backup

TODO

## FAQ

**How can I change the installation directory afterwards?**

1. Modify the configuration file.

    ```
    nano ~/AppImages/appimageinstaller/config.json
    ```
2. Move the package folder to the new location.

    ```
    mv ~/AppImages ~/AppImages_new
    ```
3. Move the .desktop files to the new location.

    This is most likely not required. If you want to do it anyway, you have to
    move all .desktop files manually.
    
    ```
    mv <old_path>/<program_id>.desktop <new_path>/<program_id>.desktop
    ```