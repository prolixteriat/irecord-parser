# irecord-parser

## Overview
This script takes as input an export from [iRecord](https://irecord.org.uk/) and applies a series of validation and transformation rules before
exporting in a format suitable for post-processing and, specifically, subsequent import to the GMEU Swift application.

## Structure
- **Code** - contains the script code.
- **Config** - contains the configuration data files used by the script (see the `config.ini` file).
- **Data_In** - contains the iRecord data to be processed.
- **Data_Out** - contains the data produced as output by the script.
- **GIS** - contains the vice-county boundary data optionally used by the script.
- **Tests** - contains automated script unit tests.

##	Installation
Installation uses the [Pipenv](https://pipenv.pypa.io/en/latest/) package manager. In order to install Pipenv if it is not already installed:

`pip install pipenv`

In order to install this project's dependencies, from within the `Code` folder run the command:

`pipenv install`

## Operation
-	The script’s runtime behaviour is configured via an INI text file. Edit the contents of the `Config\config.ini` file as required.
-	For non-standard installation, edit the contents of the `iRecord-to-Swift.bat` file as required to specify correct file paths to the `main.py` and `config.ini` files.
-	Copy one or more iRecord export CSV file(s) to be processed to the `Data_In` folder.
-	Double-click the `iRecord-to-Swift.bat` file to execute the script.
-	Progress messages will be displayed in terminal window. The same messages will also be written to the `Code\debug.log` file. 
-	Note that production of an Excel workbook containing the output results may take several minutes if you have selected that option within the `config.ini` file.
-	Once completed, you will find the output files in the `Data_Out` folder.

## Standalone Execution
- You can build a standalone executable version of the script using the following command from with the `Code` folder:
```
pyinstaller main.py --name irecord2swift --hidden-import fiona._shim --distpath <targetdir>
```
- Once created, you can use the `run.bat` batch file to execute the script.

