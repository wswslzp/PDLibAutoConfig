#!/usr/bin/python3
import logging
import argparse as ap
import jsonConfig, createTcl
import re
from qrcFinder import findQrcTechFile

def setLogLevel(args):
    if args.log_level == 'critical':
        logging.basicConfig(level=logging.CRITICAL)
    elif args.log_level == 'error':
        logging.basicConfig(level=logging.ERROR)
    elif args.log_level == 'warn':
        logging.basicConfig(level=logging.WARNING)
    elif args.log_level == 'info':
        logging.basicConfig(level=logging.INFO)
    elif args.log_level == 'debug':
        logging.basicConfig(level=logging.DEBUG)

def scan(args):
    config = jsonConfig.PdConfig()
    setLogLevel(args)
    if args.only_physic:
        config.scanIpPhysicLibs(*args.lib)
    else:
        config.addIp(*args.lib, parallel=args.multi_proc)
    if args.sdc != "":
        sdc_parser = re.compile(r"(\w+):([\w\W]+?\.sdc)")
        if sdc_parser.match(args.sdc):
            for mode, sdc in sdc_parser.findall(args.sdc):
                if mode in config.config['constraint']:
                    config.config['constraint'][mode]['sdcFile']['preCTS'] = sdc
                else:
                    config.config['constraint'][mode] = {
                        "sdcFile": {
                            "preCTS": sdc,
                            "incrCTS": "",
                            "postCTS": ""
                        }
                    }
        config.cleanConsMode()
    if args.cons is not None:
        for con in args.cons:
            mode = con[0]
            sdc = con[1]
            if mode in config.config['constraint']:
                config.config['constraint'][mode]['sdcFile']['preCTS'] = sdc
            else:
                config.config['constraint'][mode] = {
                    "sdcFile": {
                        "preCTS": sdc,
                        "incrCTS": "",
                        "postCTS": ""
                    }
                }
    if args.pdk != None:
        qrcs = findQrcTechFile(args.pdk)
        for rc in qrcs:
            config.config['rcCorner'][rc]['qrcTechFile'] = qrcs[rc]
    config.buildMmmcView()
    config.setupLef(args.metal)
    if not args.no_output:
        config.writeJson(args.output)
    if args.show_metal:
        config.showMetalAvail()
    if args.print_table != None:
        if args.print_table == 'corner':
            for tm in config.timingManager.subLibsManager:
                tm.printCornerTable()
        elif args.print_table == 'metal':
            config.physicManager.printLayers()
        elif args.print_table == 'macro':
            config.physicManager.printMacroTable()
    return args

def view(args):
    config = jsonConfig.PdConfig().readJson(args.json)
    setLogLevel(args)
    config.config['designData']['ioFile'] = args.io
    config.config['designData']['netlist'] = args.netlist
    config.writeJson(args.json)
    factory = createTcl.TclFactory(config)
    factory.printMMMCFile(args.output)
    factory.printGlobals(args.global_file)
    return args

if __name__ == "__main__":

    parser = ap.ArgumentParser()
    parser.add_argument('-v', '--version', action="version", version="v1.0")

    subparsers = parser.add_subparsers(help="choose the script stage.")

    scanParser = subparsers.add_parser("scan")
    scanParser.add_argument('-l', '--lib', help="ip lib name and dir", metavar=("<IP_LIB_NAME>", "<IP_LIB_DIR_PATH>"), nargs=2, action="append", required=True)
    scanParser.add_argument("--sdc", help="input sdc constraint file", default="", metavar="<MODE1:SDC_PATH1;MODE2:SDC_PATH2;...>")
    scanParser.add_argument("--cons", help="input modes and sdcs. can be used multiple times", action="append", nargs=2, metavar=("<MODE>", "<SDC_PATH>"))
    scanParser.add_argument("--pdk", help="The path to PDK, used to find qrctechfile", metavar="<PDK_PATH>")
    scanParser.add_argument("-o", "--output", help="output json config file name", default="config.json", metavar="<CONFIG_PATH>")
    scanParser.add_argument("--show-metal", help="show metal layer", action="store_true")
    scanParser.add_argument("--only-physic", help="only scan for physical libraries", action="store_true")
    scanParser.add_argument("--log-level", choices=['critical', 'error', 'warn', 'info', 'debug'])
    scanParser.add_argument("--multi-proc", type=int, help="enable multi-thread scanning", default=4, metavar="<NUMBER OF PROCESSOR>")
    scanParser.add_argument("--print-table", choices=['corner', 'metal', 'macro'])
    scanParser.add_argument("--metal", help="select the metal layers set")
    scanParser.add_argument("--no-output", help="Don't output json file.", action="store_true")
    scanParser.set_defaults(show_metal=False)
    scanParser.set_defaults(only_physic=False)
    scanParser.set_defaults(no_output=False)
    scanParser.set_defaults(func=scan)

    viewParser = subparsers.add_parser("view")
    viewParser.add_argument("--log-level", choices=['critical', 'error', 'warn', 'info', 'debug'])
    viewParser.add_argument("-j", "--json", help="input config json file", required=False, default="config.json",metavar="<CONFIG_PATH>")
    viewParser.add_argument("--io", help="input io file", required=False, default="", metavar="<IO_FILE>")
    viewParser.add_argument("--netlist", help="input netlist file", default="", metavar="<NETLIST_FILE>")
    viewParser.add_argument('-o', '--output', help="output view file", required=True, metavar="<OUTPUT_PATH>")
    viewParser.add_argument("-g", "--global-file", help="output global file", metavar="<GLOBALS PATH>")
    viewParser.set_defaults(func=view)

    args = parser.parse_args()
    args.func(args)
