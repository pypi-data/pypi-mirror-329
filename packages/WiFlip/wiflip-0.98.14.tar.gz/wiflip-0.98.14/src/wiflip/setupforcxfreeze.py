#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# source d'inspiration: http://wiki.wxpython.org/cx_freeze
 
import sys, os
from cx_Freeze import setup, Executable

VERSION = "12.1"
#############################################################################
# preparation des options 
company_name = 'AA55 Consulting'
product_name = 'Bibou'

includes = ["python"]

#excludes = ["openGL", "tkinter", "PyQt5"]
excludes = []
#
#packages = ["OpenGL", "OpenGL.platform"]
packages = []
build_exe_options = {'packages': packages, "includes":includes, "excludes":excludes, "optimize":1, "silent":1}

print(sys.platform)
base = None

if sys.platform == "win32":
    base = "Win32GUI"


#base = "Win32GUI"

# Create a structure for the registry table
# This will create a value 'InstallDir' in the key 'HKEY_LOCAL_MACHINE\SOFTWARE\MyCo\hello'
registry_table = [('LSystem', 2, r'SOFTWARE\AA55\LSYS', '*', None, 'TARGETDIR'),
        ('HelloInstallDir', 2, r'SOFTWARE\AA55\LSYS', 'InstallDir', '[TARGETDIR]', 'TARGETDIR'),]
# A RegLocator table to find the install directory registry key when upgrading
reg_locator_table = [('HelloInstallDirLocate', 2, r'SOFTWARE\AA55\LSYS', 'InstallDir', 0)]
# An AppSearch entry so that the MSI will search for previous installs 
# and update the default install location
app_search_table = [('TARGETDIR', 'HelloInstallDirLocate')]
# Now create the table dictionary
msi_data = {'Registry': registry_table, 'RegLocator': reg_locator_table, 'AppSearch': app_search_table}
# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'upgrade_code': '{f2581bb6-0782-459a-94da-59bdc8e07152}', # Remember to generate your own GUID for this
        'initial_target_dir': r'[ProgramFilesFolder]\AA55\LSYS', # If the registry key for install location is not found then this default directory will be used
        'data': msi_data}

bdist_dmg_options = {'volume_label': 'K'}

setup(
        name = "Bibou",
        version = VERSION,
        description = "essai avec un simple truc",
        executables = [Executable("bibou.py", 
                       icon="images/aa55_logo_2.ico",
                       base = base)],
        options = {'bdist_dmg': bdist_dmg_options, 'build_exe':build_exe_options})
# setup(
#         name = "Bibou",
#         version = VERSION,
#         description = "essai avec un simple truc",
#         executables = [Executable("bibou.py", 
#                        icon="images/aa55_logo_2.ico",
#                        base=base,
#                        shortcut_name="Bib",
#                        shortcut_dir="DesktopFolder")],
#         #options = {'bdist_msi': bdist_msi_options, 'build_exe':build_exe_options}
#     )