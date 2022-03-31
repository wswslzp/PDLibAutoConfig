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
