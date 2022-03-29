#!/usr/bin/python3
import logging
import argparse as ap
import jsonConfig, createTcl

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
        config.scanIpPhysicLibs(
            (args.ip, args.dir)
        )
    else:
        config.addIp(
            (args.ip, args.dir)
        )
    config.buildMmmcView()
    config.writeJson(args.output)
    if args.show_metal:
        config.showMetalAvail()
    return args

def view(args):
    config = jsonConfig.PdConfig().readJson(args.json)
    if args.metal != None:
        config.setupLef(args.metal)
    factory = createTcl.TclFactory(config)
    factory.printMMMCFile(args.output)
    return args

parser = ap.ArgumentParser()

subparsers = parser.add_subparsers(help="sub parser description")

scanParser = subparsers.add_parser("scan")
# scanParser.set_defaults(scanner=)
scanParser.add_argument("--ip", help="IP Name", required=True)
scanParser.add_argument("--dir", help="IP directory", required=True)
scanParser.add_argument("-o", "--output", help="output json config file name", required=False, default="config.json")
scanParser.add_argument("--show-metal", help="show metal layer", action="store_true")
scanParser.add_argument("--only-physic", help="only scan for physical libraries", action="store_true")
scanParser.add_argument("--log-level", choices=['critical', 'error', 'warn', 'info', 'debug'])
scanParser.set_defaults(show_metal=False)
scanParser.set_defaults(only_physic=False)
scanParser.set_defaults(func=scan)

viewParser = subparsers.add_parser("view")
viewParser.add_argument("-j", "--json", help="input config json file", required=False, default="config.json")
viewParser.add_argument('-o', '--output', help="output view file", required=True)
viewParser.add_argument('--metal', help="select the metal layers set")
viewParser.set_defaults(func=view)

args = parser.parse_args()
args.func(args)
