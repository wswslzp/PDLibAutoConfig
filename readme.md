# Physical Design Automaitcal Configuration

An automatical physical design configuration generation tool.

## Overview

Configuring the library setup of ASIC physical design is a tedious work, especially when there are many involved libraries.

This script is aimed to provide an automatically generated library setup script that ASIC backend tool will accept. It can relief the burden of manually work.

## Usage

The script has two step to use,
* scan step, scanning the timing and the physical library. 
* view step, generate the INNOVUS view script.

```bash
usage: main.py [-h] {scan,view} ...

positional arguments:
  {scan,view}  choose the script stage.

optional arguments:
  -h, --help   show this help message and exit
```

### Scan

The option that scan stage use,

```bash
usage: main.py scan [-h] --ip IP --dir DIR [-o OUTPUT] [--show-metal]
                    [--only-physic]
                    [--log-level {critical,error,warn,info,debug}]
                    [--multi-proc MULTI_PROC]
                    [--print-table {corner,metal,macro}]

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               IP Name
  --dir DIR             IP directory
  -o OUTPUT, --output OUTPUT
                        output json config file name
  --show-metal          show metal layer
  --only-physic         only scan for physical libraries
  --log-level {critical,error,warn,info,debug}
  --multi-proc MULTI_PROC
                        enable multi-thread scanning
  --print-table {corner,metal,macro}
```

Several options are necessary. `--ip IP` designates the IP name, and `--dir DIR` points to the IP directory where timing and physical libs reside.

`-o OUTPUT` designates the output json configuration file name. By default, it's `config.json`.

`--show-metal` is a switch option. Enabling it will show the available metal layer sets.
`--only-physic` is a switch option. Enabling it will only scan the physical libs. 

`--log-level {critical,error,warn,info,debug}` set the logging level.
`--print-table {corner,metal,macro}` set to print the table of corners, metals or available macros. This feature depends on Python package `prettytable`.

`--multi-proc MULTI_PROC` set how many CPU cores are used to parallelized the scanning procedure of timing libs. It depends on the Python package `multiprocess`.

### View 

```bash 
usage: main.py view [-h] [-j JSON] -o OUTPUT [--metal METAL]

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  input config json file
  -o OUTPUT, --output OUTPUT
                        output view file
  --metal METAL         select the metal layers set
```

`-o OUTPUT` is necessary. It designates the output view file name.

`-j JSON` set the configuration json file name. By default, it's `config.json`.

`--metal METAL` set the metal layer set that are used in PD.
