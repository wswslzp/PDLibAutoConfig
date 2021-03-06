# Physical Design Automaitcal Configuration

An automatical physical design configuration generation tool. Visit Github host page [PDlibAutoConfig](https://www.github.com/wswslzp/PDLibAutoConfig).

## Overview

Configuring the library setup of ASIC physical design is a tedious work, especially when there are many involved libraries.

This script is aimed to provide an automatically generated library setup script that ASIC backend tool will accept. It can relief the burden of manually work.

What the first part of the script actually does is to exhaustively scan the IP directories and the PDK directory to catch all the information, including the library paths, operating conditions etc. Then it will generate a JSON file that contains all those information. 

What user should do is to check the generated JSON file, and complete the design's information in the JSON file. The manual completion job is easy enough. Then the second part of the script eat the completed JSON file and generate the Innovus view file and globals file.

## Usage

The script has two step to use,
* scan step, scanning the timing and the physical library. 
* view step, generate the INNOVUS view script.

```bash
usage: main.py [-h] [-v] {scan,view} ...

positional arguments:
  {scan,view}    choose the script stage.

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

### Scan

The option that scan stage use,

```bash
usage: main.py scan [-h] -l <IP_LIB_NAME> <IP_LIB_DIR_PATH>
                    [--sdc <MODE1:SDC_PATH1;MODE2:SDC_PATH2;...>]
                    [--cons <MODE> <SDC_PATH>] [--pdk <PDK_PATH>]
                    [-o <CONFIG_PATH>] [--show-metal] [--only-physic]
                    [--log-level {critical,error,warn,info,debug}]
                    [--multi-proc <NUMBER OF PROCESSOR>]
                    [--print-table {corner,metal,macro}] [--metal METAL]
                    [--no-output]

optional arguments:
  -h, --help            show this help message and exit
  -l <IP_LIB_NAME> <IP_LIB_DIR_PATH>, --libs <IP_LIB_NAME> <IP_LIB_DIR_PATH>
                        ip lib name and dir
  --sdc <MODE1:SDC_PATH1;MODE2:SDC_PATH2;...>
                        input sdc constraint file
  --cons <MODE> <SDC_PATH>
                        input modes and sdcs. can be used multiple times
  --pdk <PDK_PATH>      The path to PDK, used to find qrctechfile
  -o <CONFIG_PATH>, --output <CONFIG_PATH>
                        output json config file name
  --show-metal          show metal layer
  --only-physic         only scan for physical libraries
  --log-level {critical,error,warn,info,debug}
  --multi-proc <NUMBER OF PROCESSOR>
                        enable multi-thread scanning
  --print-table {corner,metal,macro}
  --metal METAL         select the metal layers set
  --no-output           Don't output json file.
```

`-l` or `--libs` option designates the IP library name and directory. It can be used for multiple times to designate multiple IPs. These IP library directory should have both timing and physical libraries. This option is required.

`--sdc` input the design constraint. For multiple mode, the format it accepts is as `MODE1:SDC1;MODE2:SDC2`. For example, you have two different modes and corresponding constraints:
* `func` mode, at `~/home/Data1/hello/world/func.sdc`,
* `test` mode, at `~/home/Data1/hello/world/test.sdc`

then you should pass the option `func:~/home/Data1/hello/world/func.sdc;test:~/home/Data1/hello/world/test.sdc` to `--sdc` option. Note that the constraint file must end with `.sdc` extension.

Alternatively, option `--cons` is available too to designate the mode and the SDC files. It can be used for multiple times to designate multiple constraints.

`--pdk` input the design PDK path where the RC corner file `qrcTechFile` resides. Script will detect the corner according to the path name.

`--metal` input the selected metal layers' name. To know what names the available metal layers have, you can use the `--show-metal` to show the names.

`-o OUTPUT` designates the output json configuration file name. By default, it's `config.json`.
`--no-output` indicate the script not to produce `config.json`.

`--show-metal` is a switch option. Enabling it will show the available metal layer sets.
`--only-physic` is a switch option. Enabling it will only scan the physical libs. 

`--log-level {critical,error,warn,info,debug}` set the logging level.
`--print-table {corner,metal,macro}` set to print the table of corners, metals or available macros. This feature depends on Python package `prettytable`.

`--multi-proc MULTI_PROC` set how many CPU cores are used to parallelized the scanning procedure of timing libs. It depends on the Python package `multiprocess`.

### View 

```bash 
usage: main.py view [-h] [--log-level {critical,error,warn,info,debug}]
                    [-j <CONFIG_PATH>] [--io <IO_FILE>]
                    [--netlist <NETLIST_FILE>] -o <OUTPUT_PATH>
                    [-g <GLOBALS PATH>]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {critical,error,warn,info,debug}
  -j <CONFIG_PATH>, --json <CONFIG_PATH>
                        input config json file
  --io <IO_FILE>        input io file
  --netlist <NETLIST_FILE>
                        input netlist file
  -o <OUTPUT_PATH>, --output <OUTPUT_PATH>
                        output view file
  -g <GLOBALS PATH>, --global-file <GLOBALS PATH>
                        output global file
```
`-j JSON` set the configuration json file name. By default, it's `config.json`.

`--io` input the optional io file. `--netlist` input optional netlist file.

`-o OUTPUT` is necessary. It designates the output view file name.
`-g | --global-file` output optional `.globals` file name.
